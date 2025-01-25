import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Parameters
        checkin_date = '2025-01-27'
        checkout_date = '2025-01-31'
        url = f'https://www.booking.com/searchresults.html?ss=Spain&checkin={checkin_date}&checkout={checkout_date}&group_adults=2&no_rooms=1&group_children=0&selected_currency=EUR'

        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Set viewport size
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # Navigate to the page
        page.goto(url, timeout=60000)
        time.sleep(5)

        # Handle cookie consent
        try:
            cookie_button = page.wait_for_selector('button[aria-label="Accept"]', timeout=5000)
            if cookie_button:
                cookie_button.click()
                time.sleep(2)
        except Exception as e:
            print(f"No cookie prompt or error: {e}")

        # Handle currency selection
        try:
            currency_button = page.wait_for_selector('button[data-modal-header-async-url-param*="selected_currency=EUR"]', timeout=5000)
            if currency_button:
                currency_button.click()
                time.sleep(2)
        except Exception as e:
            print(f"No currency prompt or error: {e}")

        # Initialize variables
        hotels_list = []
        total_hotel_count = 0
        scraped_hotels = set()
        last_count = 0
        no_new_data_count = 0

        while total_hotel_count < 3000:
            # Scroll to load more content
            for _ in range(3):  # Scroll multiple times before processing
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)

            # Try to click "Load more results" button if visible
            try:
                # First try to find the button by text content
                load_more_button = page.query_selector('button:has-text("Load more results")')
                if not load_more_button:
                    # Try alternative selectors if text search fails
                    load_more_button = page.query_selector('button.a83ed08757')
                
                if load_more_button and load_more_button.is_visible():
                    print("Found 'Load more results' button, attempting to click...")
                    
                    # Try JavaScript click if regular click fails
                    try:
                        load_more_button.click(timeout=5000)
                    except:
                        page.evaluate('button => button.click()', load_more_button)
                    
                    time.sleep(5)
                    print("Successfully clicked 'Load more results' button")
            except Exception as e:
                print(f"Button interaction error: {e}")

            # Wait for hotel cards and process them
            try:
                page.wait_for_selector('div[data-testid="property-card"]', timeout=10000)
                hotels = page.query_selector_all('div[data-testid="property-card"]')
                
                current_count = len(hotels)
                print(f"Found {current_count} hotels on the current page.")
                
                if current_count == last_count:
                    no_new_data_count += 1
                    if no_new_data_count >= 3:
                        print("No new hotels loaded after multiple attempts. Trying different approach...")
                        # Try to force reload more content
                        page.evaluate("""() => {
                            window.scrollTo(0, 0);
                            setTimeout(() => {
                                window.scrollTo(0, document.body.scrollHeight);
                            }, 1000);
                        }""")
                        time.sleep(3)
                        no_new_data_count = 0
                else:
                    no_new_data_count = 0
                
                last_count = current_count

                # Process hotels
                for hotel in hotels:
                    hotel_name_elem = hotel.query_selector('div[data-testid="title"]')
                    if not hotel_name_elem:
                        continue
                        
                    hotel_name = hotel_name_elem.inner_text()
                    
                    if hotel_name in scraped_hotels:
                        continue
                    
                    scraped_hotels.add(hotel_name)
                    
                    hotel_price_elem = hotel.query_selector('span[data-testid="price-and-discounted-price"]')
                    review_score_div = hotel.query_selector('div[data-testid="review-score"]')
                    
                    hotel_price = hotel_price_elem.inner_text() if hotel_price_elem else 'No price available'
                    
                    score = 'No Score'
                    reviews_count = 'No Reviews'
                    review_text = 'No Review Text'
                    
                    if review_score_div:
                        # Get the score from the review element
                        score_elem = review_score_div.query_selector('div[class*="review-score-badge"]')
                        if score_elem:
                            score = score_elem.inner_text().strip()
                        else:
                            # Try alternative method
                            score_elements = review_score_div.query_selector_all('div')
                            if score_elements and len(score_elements) > 0:
                                raw_score = score_elements[0].inner_text()
                                score = raw_score.split()[-1]
                        
                        # Get review score and text
                        try:
                            # Get review count - using the specific class for review count text
                            reviews_div = hotel.query_selector('div.abf093bdfe.f45d8e4c32.d935416c47')
                            if reviews_div:
                                reviews_text = reviews_div.inner_text().strip()
                                # Extract only the numbers from "XXX reviews"
                                reviews_count = ''.join(filter(str.isdigit, reviews_text))
                            else:
                                reviews_count = 'No Reviews'

                            # Get review text (Wonderful/Excellent) - using the specific class
                            review_text_div = hotel.query_selector('div.a3b8729ab1.e6208ee469.cb2cbb3ccb')
                            if review_text_div:
                                review_text = review_text_div.inner_text().strip()
                            else:
                                review_text = 'No Review Text'

                        except Exception as e:
                            print(f"Error extracting review details for {hotel_name}: {e}")
                            reviews_count = 'No Reviews'
                            review_text = 'No Review Text'
                    
                    # Check for Free Cancellation
                    free_cancel_text = 'No Free Cancellation'
                    try:
                        # Look for the div with specific classes containing strong element
                        free_cancel_elem = hotel.query_selector('div.abf093bdfe strong:has-text("Free cancellation")')
                        if free_cancel_elem:
                            free_cancel_text = 'Free Cancellation'
                    except Exception as e:
                        print(f"Error checking free cancellation for {hotel_name}: {e}")

                    hotels_list.append({
                        'hotel': hotel_name,
                        'price': hotel_price,
                        'score': score,
                        'reviews_count': reviews_count,
                        'review_text': review_text,
                        'free_cancellation': free_cancel_text
                    })
                    
                    total_hotel_count += 1
                    print(f"Scraped hotel {total_hotel_count}: {hotel_name}")
                    
                    if total_hotel_count >= 3000:
                        break

            except Exception as e:
                print(f"Error processing hotels: {e}")
                break

            # Wait between iterations
            time.sleep(3)

        # Save results
        if not os.path.exists('../data'):
            os.makedirs('../data')

        df = pd.DataFrame(hotels_list)
        df.to_csv('../data/hotels_list_3000.csv', index=False)
        print(f"Data saved to data/hotels_list_3000.csv with {len(hotels_list)} hotels")

        browser.close()

if __name__ == '__main__':
    main()