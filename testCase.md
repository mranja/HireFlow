# Authentication Test Cases

| TC ID | Test Scenario | Preconditions | Test Steps | Expected Result | Priority |
|-------|---------------|---------------|------------|-----------------|----------|
| AUTH-001 | Register Admin | None | Register with Admin role | User created successfully | High |
| AUTH-002 | Register HR Manager | None | Register with HR Manager role | User created successfully | High |
| AUTH-003 | Register Recruiter | None | Register with Recruiter role | User created successfully | High |
| AUTH-004 | Register using existing email | Email already exists | Register again with the same email | **409 Conflict** returned | High |
| AUTH-005 | Missing email | None | Leave email field empty and submit | **400 Bad Request** returned | High |
| AUTH-006 | Invalid email format | None | Enter an invalid email format (e.g., `user@`) | Validation error returned | High |
| AUTH-007 | Missing password | None | Leave password field blank | Validation error returned | High |
| AUTH-008 | Weak password | None | Enter password as `123` | Validation error for weak password | Medium |
| AUTH-009 | Successful Login | User is already registered | Login with valid email and password | JWT token generated successfully | High |
| AUTH-010 | Wrong password | Registered user | Login with incorrect password | **401 Unauthorized** returned | High |
| AUTH-011 | Wrong email | None | Login using an unregistered email | User not found / **401 Unauthorized** | High |
| AUTH-012 | Empty login fields | None | Leave email and password fields empty | Validation error returned | Medium |
| AUTH-013 | JWT Expiry | Logged in | Access API using an expired JWT | **401 Unauthorized** returned | High |
| AUTH-014 | Access protected API without token | None | Send `GET /candidates` request without JWT | **401 Unauthorized** returned | High |
| AUTH-015 | Access protected API with valid JWT | Logged in | Send `GET /candidates` with valid JWT | Request succeeds with **200 OK** | High |
| AUTH-016 | Invalid JWT | None | Send request using an invalid/fake JWT | **401 Unauthorized** returned | High |
| AUTH-017 | Recruiter accessing Admin API | Recruiter logged in | Send `POST /departments` request | **403 Forbidden** returned | High |
| AUTH-018 | HR Manager accessing Admin API | HR Manager logged in | Send `DELETE /departments` request | **403 Forbidden** returned | High |
| AUTH-019 | Admin accessing Admin API | Admin logged in | Send `POST /departments` request | Department created successfully | High |
| AUTH-020 | Logout (Client Side) | Logged in | Remove JWT token and attempt protected API | Session ends and protected APIs are inaccessible | Medium |
