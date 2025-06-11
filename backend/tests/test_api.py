"""
API endpoint tests for URL shortener.
"""
import pytest
from fastapi.testclient import TestClient


class TestURLAPI:
    """Test URL API endpoints."""
    
    def test_create_url_success(self, client: TestClient, sample_url_data):
        """Test successful URL creation."""
        response = client.post("/api/urls", json=sample_url_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert "short_code" in data
        assert "original_url" in data
        assert data["original_url"] == sample_url_data["original_url"]
        assert data["click_count"] == 0
    
    def test_create_url_invalid(self, client: TestClient, invalid_url_data):
        """Test URL creation with invalid URL."""
        response = client.post("/api/urls", json=invalid_url_data)
        assert response.status_code == 400
        assert "Invalid URL format" in response.json()["detail"]
    
    def test_get_urls_empty(self, client: TestClient):
        """Test getting URLs when none exist."""
        response = client.get("/api/urls")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_urls_with_data(self, client: TestClient, sample_url_data):
        """Test getting URLs after creating one."""
        # Create a URL first
        create_response = client.post("/api/urls", json=sample_url_data)
        assert create_response.status_code == 200
        
        # Get URLs
        response = client.get("/api/urls")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["original_url"] == sample_url_data["original_url"]
    
    def test_get_url_by_short_code(self, client: TestClient, sample_url_data):
        """Test getting URL by short code."""
        # Create a URL first
        create_response = client.post("/api/urls", json=sample_url_data)
        short_code = create_response.json()["short_code"]
        
        # Get URL by short code
        response = client.get(f"/api/urls/{short_code}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["short_code"] == short_code
        assert data["original_url"] == sample_url_data["original_url"]
    
    def test_get_url_not_found(self, client: TestClient):
        """Test getting non-existent URL."""
        response = client.get("/api/urls/nonexistent")
        assert response.status_code == 404
        assert "URL not found" in response.json()["detail"]
    
    def test_redirect_url(self, client: TestClient, sample_url_data):
        """Test URL redirection."""
        # Create a URL first
        create_response = client.post("/api/urls", json=sample_url_data)
        short_code = create_response.json()["short_code"]
        
        # Test redirect (don't follow redirects to test the response)
        response = client.get(f"/r/{short_code}", follow_redirects=False)
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == sample_url_data["original_url"]
    
    def test_redirect_not_found(self, client: TestClient):
        """Test redirect for non-existent URL."""
        response = client.get("/r/nonexistent")
        assert response.status_code == 404
        assert "URL not found" in response.json()["detail"]
    
    def test_get_clicks(self, client: TestClient, sample_url_data):
        """Test getting click history."""
        # Create a URL first
        create_response = client.post("/api/urls", json=sample_url_data)
        short_code = create_response.json()["short_code"]
        
        # Get clicks (should be empty initially)
        response = client.get(f"/api/urls/{short_code}/clicks")
        assert response.status_code == 200
        assert response.json() == []
        
        # Make a redirect to create a click
        client.get(f"/r/{short_code}", follow_redirects=False)
        
        # Get clicks again (should have one click now)
        response = client.get(f"/api/urls/{short_code}/clicks")
        assert response.status_code == 200
        
        clicks = response.json()
        assert len(clicks) == 1
        assert "timestamp" in clicks[0]
        assert "client_ip" in clicks[0]
    
    def test_get_stats(self, client: TestClient, sample_url_data):
        """Test getting application statistics."""
        # Get stats when empty
        response = client.get("/api/stats")
        assert response.status_code == 200
        
        stats = response.json()
        assert "total_urls" in stats
        assert "total_clicks" in stats
        assert stats["total_urls"] == 0
        assert stats["total_clicks"] == 0
        
        # Create a URL and check stats again
        client.post("/api/urls", json=sample_url_data)
        
        response = client.get("/api/stats")
        assert response.status_code == 200
        
        stats = response.json()
        assert stats["total_urls"] == 1
        assert stats["total_clicks"] == 0


class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json() 