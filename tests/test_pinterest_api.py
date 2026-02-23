"""Tests for Pinterest API URL parsing."""

from pinterest_dl.api.api import Api
from pinterest_dl.exceptions import (
    InvalidBoardUrlError,
    InvalidPinterestUrlError,
    InvalidSearchUrlError,
)


class TestPinterestAPIUrlParsing:
    """Test URL parsing methods in Api."""

    def test_parse_pin_id_valid_url(self):
        """Test parsing pin ID from valid Pinterest URL."""
        api = Api("https://www.pinterest.com/pin/123456789012345/")
        assert api.pin_id == "123456789012345"

    def test_parse_pin_id_without_trailing_slash(self):
        """Test parsing pin ID - URL needs trailing slash."""
        # Note: The API requires trailing slash, so this will be None
        api = Api("https://www.pinterest.com/pin/987654321098765")
        # Without trailing slash, it won't parse
        assert api.pin_id is None

    def test_parse_board_url_valid(self):
        """Test parsing board URL."""
        api = Api("https://www.pinterest.com/username/board-name/")
        assert api.username == "username"
        assert api.boardname == "board-name"

    def test_parse_board_url_without_trailing_slash(self):
        """Test parsing board URL without trailing slash."""
        api = Api("https://www.pinterest.com/testuser/my-board")
        assert api.username == "testuser"
        assert api.boardname == "my-board"

    def test_parse_search_query_url(self):
        """Test parsing search query from URL."""
        api = Api("https://www.pinterest.com/search/pins/?q=nature&rs=typed")
        assert api.query == "nature"

    def test_invalid_url_sets_none(self):
        """Test that invalid URLs set attributes to None."""
        api = Api("https://www.pinterest.com/")
        assert api.pin_id is None
        assert api.query is None

    def test_is_pin_property(self):
        """Test is_pin attribute."""
        pin_api = Api("https://www.pinterest.com/pin/123456789012345/")
        assert pin_api.is_pin is True

        board_api = Api("https://www.pinterest.com/user/board/")
        assert board_api.is_pin is False

    def test_board_attributes_set(self):
        """Test board username and boardname are set correctly."""
        board_api = Api("https://www.pinterest.com/user/myboard/")
        assert board_api.username == "user"
        assert board_api.boardname == "myboard"

    def test_search_query_attribute(self):
        """Test search query attribute is set."""
        search_api = Api("https://www.pinterest.com/search/pins/?q=nature&rs=typed")
        assert search_api.query == "nature"

    def test_parse_section_url_valid(self):
        """Test parsing section URL with 3 path segments."""
        api = Api("https://id.pinterest.com/Murasaki_Akiyama/wallpaper/live-wallpaper/")
        assert api.username == "Murasaki_Akiyama"
        assert api.boardname == "wallpaper"
        assert api.section_slug == "live-wallpaper"
        assert api.is_section is True

    def test_parse_section_url_without_trailing_slash(self):
        """Test parsing section URL without trailing slash."""
        api = Api("https://www.pinterest.com/testuser/my-board/my-section")
        assert api.username == "testuser"
        assert api.boardname == "my-board"
        assert api.section_slug == "my-section"
        assert api.is_section is True

    def test_board_url_is_not_section(self):
        """Test that regular board URL is not detected as section."""
        api = Api("https://www.pinterest.com/username/boardname/")
        assert api.is_section is False
        assert api.section_slug is None

    def test_section_url_with_different_subdomains(self):
        """Test section URL with various Pinterest subdomains."""
        # Japanese subdomain
        api = Api("https://jp.pinterest.com/user/board/section/")
        assert api.is_section is True
        assert api.section_slug == "section"

        # German subdomain
        api2 = Api("https://de.pinterest.com/user/board/section/")
        assert api2.is_section is True
        assert api2.section_slug == "section"

    def test_cyrillic_board_url(self):
        """Test parsing Cyrillic board URL with URL encoding."""
        api = Api("https://ru.pinterest.com/testuser/%D1%84%D1%80%D0%B5%D0%B3%D0%B0%D1%82-%D0%BE%D1%80%D0%B5%D0%BB/")
        assert api.username == "testuser"
        assert api.boardname == "фрегат-орел"
        assert api.is_section is False

    def test_cyrillic_section_url(self):
        """Test parsing Cyrillic section URL with URL encoding."""
        api = Api("https://ru.pinterest.com/testuser/%D1%84%D1%80%D0%B5%D0%B3%D0%B0%D1%82-%D0%BE%D1%80%D0%B5%D0%BB/%D0%BC%D0%BE%D1%80%D0%B5/")
        assert api.username == "testuser"
        assert api.boardname == "фрегат-орел"
        assert api.section_slug == "море"
        assert api.is_section is True

    def test_mixed_ascii_cyrillic_board_url(self):
        """Test parsing board URL with mixed ASCII and Cyrillic characters."""
        api = Api("https://ru.pinterest.com/user123/board-%D1%84%D1%80%D0%B5%D0%B3%D0%B0%D1%82/")
        assert api.username == "user123"
        assert api.boardname == "board-фрегат"
        assert api.is_section is False

    def test_cyrillic_board_url_without_trailing_slash(self):
        """Test parsing Cyrillic board URL without trailing slash."""
        api = Api("https://ru.pinterest.com/testuser/%D1%84%D1%80%D0%B5%D0%B3%D0%B0%D1%82-%D0%BE%D1%80%D0%B5%D0%BB")
        assert api.username == "testuser"
        assert api.boardname == "фрегат-орел"

    def test_cyrillic_section_url_without_trailing_slash(self):
        """Test parsing Cyrillic section URL without trailing slash."""
        api = Api("https://ru.pinterest.com/testuser/%D1%84%D1%80%D0%B5%D0%B3%D0%B0%D1%82-%D0%BE%D1%80%D0%B5%D0%BB/%D0%BC%D0%BE%D1%80%D0%B5")
        assert api.username == "testuser"
        assert api.boardname == "фрегат-орел"
        assert api.section_slug == "море"
        assert api.is_section is True

    def test_cyrillic_with_underscore_and_hyphen(self):
        """Test Cyrillic URLs with underscores and hyphens."""
        api = Api("https://ru.pinterest.com/testuser_%D1%82%D0%B5%D1%81%D1%82/board-%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80/")
        assert api.username == "testuser_тест"
        assert api.boardname == "board-пример"

    def test_multiple_cyrillic_sections(self):
        """Test multiple Cyrillic sections in URL."""
        api = Api("https://ru.pinterest.com/%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C/%D0%B4%D0%BE%D1%81%D0%BA%D0%B0/%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB/")
        assert api.username == "пользователь"
        assert api.boardname == "доска"
        assert api.section_slug == "раздел"
        assert api.is_section is True
