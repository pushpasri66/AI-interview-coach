import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from app import create_app
from backend.database import db
from backend.models.user import User

def test_phase1():
    print("--- Starting Phase 1 Verification Test ---")

    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True

    client = app.test_client()

    with app.app_context():
        # 1. Verify DB Table creation
        db.create_all()
        print("[OK] Database tables created successfully.")

        # 2. Clean existing test user if present
        existing = User.query.filter_by(email="testuser@example.com").first()
        if existing:
            db.session.delete(existing)
            db.session.commit()

        # 3. Test Registration via Route
        response = client.post("/register", data={
            "fullname": "Test Candidate",
            "email": "testuser@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!"
        }, follow_redirects=True)

        assert response.status_code == 200, f"Registration failed with status code {response.status_code}"
        print("[OK] User registration POST request successful.")

        # Verify DB entry
        user = User.query.filter_by(email="testuser@example.com").first()
        assert user is not None, "User not found in database!"
        assert user.check_password("Password123!"), "Password hash verification failed!"
        assert not user.check_password("WrongPassword"), "Invalid password check failed!"
        print(f"[OK] User stored in database: ID={user.id}, Name={user.fullname}, Hashed Password Verified.")

        # 4. Test Unauthenticated Protected Route Access (Dashboard redirect to Login)
        dash_response = client.get("/dashboard", follow_redirects=False)
        assert dash_response.status_code == 302, "Unauthenticated access to /dashboard should redirect!"
        assert "/login" in dash_response.headers["Location"], "Redirect should point to login page!"
        print("[OK] Protected route /dashboard correctly redirected unauthenticated request to /login.")

        # 5. Test Login via Route
        login_resp = client.post("/login", data={
            "email": "testuser@example.com",
            "password": "Password123!"
        }, follow_redirects=True)

        assert login_resp.status_code == 200
        assert b"Welcome back, Test Candidate!" in login_resp.data or b"Dashboard" in login_resp.data
        print("[OK] User login session established & redirected to Dashboard.")

        # 6. Test Profile Update
        prof_resp = client.post("/profile", data={
            "action": "update_profile",
            "fullname": "Updated Candidate Name"
        }, follow_redirects=True)
        assert prof_resp.status_code == 200
        updated_user = User.query.filter_by(email="testuser@example.com").first()
        assert updated_user.fullname == "Updated Candidate Name"
        print("[OK] Profile full name update successful.")

        # 7. Test Logout Route
        logout_resp = client.get("/logout", follow_redirects=True)
        assert logout_resp.status_code == 200
        print("[OK] Logout successful.")

        # 8. Verify Log File Created
        log_file = os.path.join(app.root_path, "..", "logs", "app.log")
        assert os.path.exists(log_file), "Log file logs/app.log was not created!"
        print(f"[OK] Application logging verified at {log_file}.")

        print("\nALL PHASE 1 VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_phase1()
