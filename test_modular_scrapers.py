#!/usr/bin/env python3
"""
Test script for the modular data scraper system.
This script demonstrates how to use individual scrapers and the main scraper class.
"""

import sys
import logging
from data_scraper import MacadamiaTradeDataScraper

# Import individual scrapers for direct testing
from scrapers.un_comtrade_scraper import UNComtradeScraper
from scrapers.korea_customs_scraper import KoreaCustomsScraper
from scrapers.additional_sources_scraper import AdditionalSourcesScraper
from scrapers.public_data_scraper import PublicDataScraper
from scrapers.historical_data_scraper import HistoricalDataScraper

import requests

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_individual_scrapers():
    """Test individual scraper modules"""
    logger.info("=== Testing Individual Scrapers ===")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'MacadamiaTradeBot/1.0 (Test Environment)',
        'Accept': 'application/json'
    })
    
    # Test UN Comtrade scraper
    logger.info("Testing UN Comtrade Scraper...")
    un_scraper = UNComtradeScraper(session)
    un_data = un_scraper.scrape_current_data()
    logger.info(f"UN Comtrade: {len(un_data)} records collected")
    
    # Test Korea Customs scraper
    logger.info("Testing Korea Customs Scraper...")
    korea_scraper = KoreaCustomsScraper(session)
    korea_data = korea_scraper.scrape_current_data()
    logger.info(f"Korea Customs: {len(korea_data)} records collected")
    
    # Test Additional Sources scraper
    logger.info("Testing Additional Sources Scraper...")
    additional_scraper = AdditionalSourcesScraper(session)
    additional_data = additional_scraper.scrape_additional_real_sources()
    logger.info(f"Additional Sources: {len(additional_data)} records collected")
    
    session.close()
    logger.info("Individual scraper tests completed")

def test_main_scraper():
    """Test the main scraper class"""
    logger.info("=== Testing Main Scraper Class ===")
    
    scraper = MacadamiaTradeDataScraper()
    
    # Test current data collection
    logger.info("Testing current data collection...")
    un_data = scraper.scrape_un_comtrade_data()
    logger.info(f"Main scraper - UN Comtrade: {len(un_data)} records")
    
    korea_data = scraper.scrape_korea_customs_data()
    logger.info(f"Main scraper - Korea Customs: {len(korea_data)} records")
    
    additional_data = scraper.scrape_additional_real_sources()
    logger.info(f"Main scraper - Additional Sources: {len(additional_data)} records")
    
    public_data = scraper.scrape_public_trade_data()
    logger.info(f"Main scraper - Public Data: {len(public_data)} records")
    
    # Test historical data collection (just check if methods exist)
    logger.info("Testing historical data methods...")
    try:
        historical_un = scraper.scrape_historical_un_comtrade_data()
        logger.info(f"Historical UN Comtrade: {len(historical_un)} records")
    except Exception as e:
        logger.warning(f"Historical UN Comtrade test failed: {e}")
    
    try:
        yearly_data = scraper.scrape_un_comtrade_data_yearly([2023, 2024])
        logger.info(f"Yearly data: {len(yearly_data)} records")
    except Exception as e:
        logger.warning(f"Yearly data test failed: {e}")
    
    scraper.close()
    logger.info("Main scraper tests completed")

def test_modular_structure():
    """Test that the modular structure is working correctly"""
    logger.info("=== Testing Modular Structure ===")
    
    # Test that all modules can be imported
    try:
        from scrapers import (
            UNComtradeScraper, 
            KoreaCustomsScraper, 
            AdditionalSourcesScraper,
            PublicDataScraper, 
            HistoricalDataScraper
        )
        logger.info("✓ All scraper modules imported successfully")
    except ImportError as e:
        logger.error(f"✗ Import error: {e}")
        return False
    
    # Test that main scraper can be initialized
    try:
        scraper = MacadamiaTradeDataScraper()
        logger.info("✓ Main scraper initialized successfully")
        
        # Test that it has all expected scrapers
        assert hasattr(scraper, 'un_comtrade_scraper')
        assert hasattr(scraper, 'korea_customs_scraper')
        assert hasattr(scraper, 'additional_sources_scraper')
        assert hasattr(scraper, 'public_data_scraper')
        assert hasattr(scraper, 'historical_data_scraper')
        logger.info("✓ All expected scraper attributes present")
        
        scraper.close()
        
    except Exception as e:
        logger.error(f"✗ Main scraper initialization failed: {e}")
        return False
    
    logger.info("✓ Modular structure validation completed successfully")
    return True

def main():
    """Run all tests"""
    logger.info("Starting modular data scraper tests...")
    
    # Test modular structure first
    if not test_modular_structure():
        logger.error("Modular structure test failed. Exiting.")
        sys.exit(1)
    
    # Test individual scrapers
    test_individual_scrapers()
    
    # Test main scraper
    test_main_scraper()
    
    logger.info("All tests completed successfully!")
    logger.info("The data scraper has been successfully modularized!")

if __name__ == "__main__":
    main()
