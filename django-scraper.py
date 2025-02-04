from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.utils import timezone
from ..models import Page, Post, SocialMediaUser
from .storage import upload_to_s3
import asyncio
import logging

logger = logging.getLogger(__name__)

class FacebookScraper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

    def scrape_page(self, username: str) -> Page:
        driver = webdriver.Chrome(options=self.options)
        try:
            # Navigate to page
            driver.get(f"https://www.facebook.com/{username}")
            driver.implicitly_wait(5)
            
            # Extract basic page info
            page_data = {
                'username': username,
                'name': self._get_element_text(driver, "//h1"),
                'facebook_id': self._extract_page_id(driver),
                'url': driver.current_url,
                'profile_pic_url': self._get_profile_pic(driver),
                'category': self._get_element_text(driver, "//div[@data-key='page_category']"),
                'followers_count': self._extract_followers_count(driver),
                'likes_count': self._extract_likes_count(driver),
                'created_at': timezone.now(),
            }
            
            # Upload profile pic to S3
            page_data['profile_pic_s3_url'] = upload_to_s3(
                page_data['profile_pic_url'], 
                f"pages/{username}/profile.jpg"
            )
            
            # Create or update page
            page, created = Page.objects.update_or_create(
                username=username,
                defaults=page_data
            )
            
            # Scrape posts
            self._scrape_posts(driver, page)
            
            return page
            
        except Exception as e:
            logger.error(f"Error scraping page {username}: {str(e)}")
            raise
        finally:
            driver.quit()

    def _scrape_posts(self, driver, page: Page, limit: int = 25):
        post_elements = driver.find_elements(By.XPATH, "//div[@data-testid='post_container']")
        
        for element in post_elements[:limit]:
            try:
                post_data = {
                    'facebook_id': element.get_attribute("id"),
                    'content': self._get_post_content(element),
                    'posted_at': self._get_post_date(element),
                    'likes_count': self._get_post_likes(element),
                    'comments_count': self._get_post_comments(element),
                    'media_urls': self._get_post_media(element),
                    'page': page
                }
                
                # Upload media to S3
                post_data['media_s3_urls'] = []
                for idx, url in enumerate(post_data['media_urls']):
                    s3_url = upload_to_s3(
                        url, 
                        f"pages/{page.username}/posts/{post_data['facebook_id']}/media_{idx}.jpg"
                    )
                    post_data['media_s3_urls'].append(s3_url)
                
                Post.objects.update_or_create(
                    facebook_id=post_data['facebook_id'],
                    defaults=post_data
                )
            
            except Exception as e:
                logger.error(f"Error scraping post: {str(e)}")
                continue

    # Helper methods implementations remain similar to FastAPI version
    def _get_element_text(self, driver, xpath: str) -> str:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element.text
        except:
            return ""

    def _extract_page_id(self, driver) -> str:
        # Implementation to extract page ID
        pass

    def _get_profile_pic(self, driver) -> str:
        # Implementation to get profile picture URL
        pass

    def _extract_followers_count(self, driver) -> int:
        # Implementation to extract followers count
        pass

    def _extract_likes_count(self, driver) -> int:
        # Implementation to extract likes count
        pass
