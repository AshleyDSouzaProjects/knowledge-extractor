"""
Tweet Thread Extractor for /kua

Integrated into knowledge extractor to handle "tweet thread" mode:
- Detects "tweet thread" marker in pending file comments
- Collects author continuations OR top 5 replies
- Synthesizes into 250-750 word note based on content depth
- Files as merged thread note to vault

Usage:
    from tweet_thread_extractor import TweetThreadExtractor

    extractor = TweetThreadExtractor(twitter_api_client, claude_client)
    result = extractor.process_thread(url, pending_comments)
    # Returns: {'status': 'Done!', 'note_path': ..., 'thread_depth': N, ...}
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Optional


class TweetThreadExtractor:

    def __init__(self, twitter_api_client=None, claude_client=None):
        self.twitter_client = twitter_api_client
        self.claude_client = claude_client
        self.vault_path = '/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault'

    def process_thread(self, tweet_url, pending_comments=None):
        """Main entry point: URL -> collected tweets -> synthesis -> filed note"""

        tweet_id = self.extract_tweet_id(tweet_url)
        if not tweet_id:
            return {'status': 'error', 'message': 'Could not extract tweet ID'}

        main_tweet = self.fetch_tweet(tweet_id)
        if not main_tweet:
            return {'status': 'error', 'message': 'Could not fetch main tweet'}

        thread_type = self.detect_thread_type(main_tweet)
        related_tweets = self.collect_related_tweets(main_tweet, thread_type)

        tweet_texts = [main_tweet] + related_tweets

        synthesis = self.create_synthesis(tweet_texts, pending_comments, thread_type)
        note_content = self.assemble_note(tweet_texts, synthesis)
        note_path = self.write_note(note_content, main_tweet, thread_type)

        return {
            'status': 'Done!',
            'note_path': note_path,
            'thread_depth': len(tweet_texts),
            'engagement': self.calculate_engagement(tweet_texts),
            'synthesis_length': len(synthesis.split()),
            'filename': os.path.basename(note_path) if note_path else None
        }

    def extract_tweet_id(self, url):
        """Parse tweet ID from X/Twitter URL"""
        patterns = [r'x\.com/.*?/status/(\d+)', r'twitter\.com/.*?/status/(\d+)']
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def fetch_tweet(self, tweet_id):
        """Fetch tweet details via Twitter API (or mock if no client)"""
        if not self.twitter_client:
            return {
                'id': tweet_id,
                'text': '[Tweet content unavailable without API]',
                'author': 'unknown',
                'metrics': {'like_count': 0, 'retweet_count': 0},
                'created_at': '',
                'conversation_id': tweet_id
            }

        try:
            tweet = self.twitter_client.get_tweet(
                id=tweet_id,
                tweet_fields=['created_at', 'public_metrics', 'conversation_id', 'in_reply_to_user_id'],
                expansions=['author_id'],
                user_fields=['username', 'name']
            )

            author_info = tweet.includes['users'][0] if tweet.includes and 'users' in tweet.includes else {}

            return {
                'id': tweet_id,
                'text': tweet.data['text'],
                'author': author_info.get('username', 'unknown'),
                'author_name': author_info.get('name', ''),
                'created_at': tweet.data.get('created_at', ''),
                'metrics': tweet.data['public_metrics'],
                'conversation_id': tweet.data.get('conversation_id', tweet_id),
                'in_reply_to_user_id': tweet.data.get('in_reply_to_user_id')
            }
        except Exception as e:
            print(f'Error fetching tweet {tweet_id}: {e}')
            return None

    def detect_thread_type(self, main_tweet):
        """Determine if author thread or community discussion"""
        if main_tweet.get('in_reply_to_user_id'):
            return 'community_discussion'
        return 'author_thread'

    def collect_related_tweets(self, main_tweet, thread_type):
        """Collect author continuations or top 5 replies"""
        if not self.twitter_client:
            return []

        try:
            if thread_type == 'author_thread':
                return self.fetch_author_continuation(main_tweet)
            else:
                return self.fetch_top_replies(main_tweet['id'])
        except Exception as e:
            print(f'Error collecting related tweets: {e}')
            return []

    def fetch_author_continuation(self, main_tweet):
        """Fetch all tweets from author in same thread"""
        try:
            author_id = main_tweet.get('author', '')
            conversation_id = main_tweet['conversation_id']

            author_tweets = self.twitter_client.search_recent_tweets(
                query=f'from:{author_id} conversation_id:{conversation_id}',
                tweet_fields=['created_at', 'public_metrics'],
                expansions=['author_id'],
                user_fields=['username'],
                max_results=100
            )

            if not author_tweets.data:
                return []

            sorted_tweets = sorted(author_tweets.data, key=lambda t: t['created_at'])
            return [self.format_tweet(t, 'author_continuation') for t in sorted_tweets if t['id'] != main_tweet['id']]
        except Exception as e:
            print(f'Error fetching author continuation: {e}')
            return []

    def fetch_top_replies(self, tweet_id):
        """Fetch top 5 replies by engagement"""
        try:
            replies = self.twitter_client.search_recent_tweets(
                query=f'conversation_id:{tweet_id}',
                tweet_fields=['public_metrics', 'created_at'],
                expansions=['author_id'],
                user_fields=['username'],
                max_results=100
            )

            if not replies.data:
                return []

            sorted_replies = sorted(
                replies.data,
                key=lambda t: t['public_metrics']['like_count'] + t['public_metrics']['retweet_count'],
                reverse=True
            )

            return [self.format_tweet(t, 'reply') for t in sorted_replies[:5]]
        except Exception as e:
            print(f'Error fetching replies: {e}')
            return []

    def format_tweet(self, tweet_obj, tweet_type='reply'):
        """Standardize tweet object"""
        return {
            'id': tweet_obj['id'],
            'text': tweet_obj['text'],
            'author': tweet_obj.get('author_username', 'unknown'),
            'metrics': tweet_obj.get('public_metrics', {}),
            'type': tweet_type
        }

    def create_synthesis(self, tweet_texts, pending_comments, thread_type):
        """Create 250-750 word synthesis based on depth"""
        depth = self.estimate_depth(tweet_texts)

        if depth == 'shallow':
            target_length = 250
        elif depth == 'medium':
            target_length = 400
        else:
            target_length = 650

        synthesis_parts = []
        synthesis_parts.append('Main Thesis')
        synthesis_parts.append(tweet_texts[0]['text'])
        synthesis_parts.append('')

        if len(tweet_texts) > 1:
            author_tweets = [t for t in tweet_texts[1:] if t.get('type') != 'reply']
            if author_tweets:
                synthesis_parts.append('Author Development')
                for tweet in author_tweets:
                    synthesis_parts.append('- ' + tweet['text'][:150])
                synthesis_parts.append('')

        reply_tweets = [t for t in tweet_texts if t.get('type') == 'reply']
        if reply_tweets:
            synthesis_parts.append('Key Responses')
            for reply in reply_tweets[:3]:
                synthesis_parts.append('- ' + reply.get('author', 'unknown') + ': ' + reply['text'][:100])
            synthesis_parts.append('')

        synthesis = '\n'.join(synthesis_parts)

        if self.claude_client and len(synthesis.split()) < target_length:
            extended = self.call_claude_for_synthesis(tweet_texts, target_length)
            if extended:
                synthesis = extended

        return synthesis

    def estimate_depth(self, tweet_texts):
        """Classify thread as shallow/medium/deep based on content"""
        if len(tweet_texts) < 2:
            return 'shallow'

        engagement = self.calculate_engagement(tweet_texts)
        text_length = sum(len(t.get('text', '')) for t in tweet_texts)

        if engagement < 500 and text_length < 800:
            return 'shallow'
        elif engagement < 2000 or text_length < 2000:
            return 'medium'
        else:
            return 'deep'

    def call_claude_for_synthesis(self, tweet_texts, target_length):
        """Use Claude to create extended synthesis"""
        if not self.claude_client:
            return None

        tweets_str = '\n\n'.join([
            f"Tweet {i+1}:\n{t.get('text', '')} (by {t.get('author', 'unknown')})"
            for i, t in enumerate(tweet_texts)
        ])

        prompt = f"""Synthesize this Twitter thread ({target_length} words).

TWEETS:
{tweets_str}

Create focused synthesis:
1. Main thesis clearly stated
2. Author's key points/evolution (if multi-part)
3. Important replies/disagreements
4. Actionable insight or implication

Target: approximately {target_length} words."""

        try:
            response = self.claude_client.messages.create(
                model='claude-opus-4-8',
                max_tokens=500,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f'Error calling Claude: {e}')
            return None

    def assemble_note(self, tweet_texts, synthesis):
        """Assemble markdown note with all content"""
        lines = []

        main = tweet_texts[0]
        topic = self.extract_topic(main['text'])

        lines.append(f"# Tweet Thread: {topic}\n")
        lines.append(f"By {main.get('author', 'unknown')} | {main.get('created_at', 'unknown date')}\n")
        lines.append(f"Engagement: {self.calculate_engagement(tweet_texts)} combined likes\n")
        lines.append('\n---\n')

        lines.append('\n## Original Tweet\n')
        lines.append(main['text'] + '\n')
        lines.append(f"\nLikes: {main.get('metrics', {}).get('like_count', 0)}\n")

        author_continuations = [t for t in tweet_texts[1:] if t.get('type') != 'reply']
        if author_continuations:
            lines.append('\n## Author\'s Thread\n')
            for i, tweet in enumerate(author_continuations, 2):
                lines.append(f"### Part {i}\n{tweet['text']}\n")

        replies = [t for t in tweet_texts if t.get('type') == 'reply']
        if replies:
            lines.append('\n## Community Responses\n')
            for reply in replies:
                lines.append(f"### {reply.get('author', 'unknown')}\n{reply['text']}\n")
                lines.append(f"*{reply.get('metrics', {}).get('like_count', 0)} likes*\n")

        lines.append('\n---\n\n## Analysis\n')
        lines.append(synthesis + '\n')

        return ''.join(lines)

    def extract_topic(self, text):
        """Extract topic from first few words"""
        words = text.split()[:8]
        return ' '.join(words).strip('.,!?')

    def calculate_engagement(self, tweets):
        """Sum likes across all tweets"""
        total = 0
        for tweet in tweets:
            metrics = tweet.get('metrics', {})
            total += metrics.get('like_count', 0)
        return total

    def write_note(self, content, main_tweet, thread_type):
        """Write note to vault with frontmatter"""
        filename = self.generate_filename(main_tweet)
        filepath = os.path.join(self.vault_path, 'AI/06-resources', filename)

        frontmatter = f"""---
tags: [tweet-thread, twitter, discussion]
source: https://x.com/{main_tweet.get('author', 'unknown')}/status/{main_tweet['id']}
date: {datetime.now().isoformat()}
thread_type: {thread_type}
---

"""

        try:
            with open(filepath, 'w') as f:
                f.write(frontmatter + content)
            return filepath
        except Exception as e:
            print(f'Error writing note: {e}')
            return None

    def generate_filename(self, main_tweet):
        """Generate filename: thread-{author}-{topic}-{date}.md"""
        author = main_tweet.get('author', 'unknown')
        topic = self.extract_topic(main_tweet['text']).lower().replace(' ', '-')[:30]
        date = datetime.now().strftime('%Y%m%d')

        return f"thread-{author}-{topic}-{date}.md"
