import unittest

from httpx import ASGITransport, AsyncClient

from creation_workbench.api.app import create_app


class HealthTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = AsyncClient(transport=ASGITransport(app=create_app()), base_url="http://test")
        self.addAsyncCleanup(self.client.aclose)

    async def test_live_is_independent_of_missing_runtime(self):
        self.assertEqual((await self.client.get("/health/live")).status_code, 200)
        ready = await self.client.get("/health/ready")
        self.assertEqual(ready.status_code, 503)
        self.assertEqual(ready.json()["reason"], "runtime_not_configured")

    async def test_capabilities_do_not_claim_generation_or_persistence(self):
        response = await self.client.get("/api/v1/capabilities")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["stage"], "B00")
        for key in ("runtime_connected", "creation_enabled", "persistence_enabled"):
            self.assertIs(data[key], False)

    async def test_no_unimplemented_business_write_is_exposed(self):
        response = await self.client.post("/api/v1/projects", json={})
        self.assertEqual(response.status_code, 404)

    async def test_openapi_has_bootstrap_routes(self):
        paths = (await self.client.get("/openapi.json")).json()["paths"]
        self.assertEqual(set(paths), {"/health/live", "/health/ready", "/api/v1/capabilities"})
