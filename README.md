# HireFlow Analytics

## Overview

HireFlow Analytics is a recruitment analytics platform designed to centralize candidate, interview, and department data into a single dashboard. The platform enables recruiters, HR managers, and administrators to monitor recruitment performance, analyze hiring metrics, identify pipeline bottlenecks, and generate detailed reports for data-driven decision-making.

---

## Problem Statement

Recruitment data is often scattered across multiple systems, making it difficult for organizations to answer critical hiring questions such as:

- Where candidates drop off during the recruitment process
- Why candidates reject offers
- Which departments hire most efficiently
- Which interviewers perform best
- How long the hiring process takes

HireFlow Analytics addresses these challenges by providing a centralized recruitment management and analytics platform.

---

## Features

### Authentication & Authorization

- User Registration
- User Login
- JWT-based Authentication
- Role-Based Access Control (RBAC)
- Secure Password Hashing

### Candidate Management

- Create, Read, Update, and Delete Candidates
- Resume Upload
- Search Candidates
- Pagination
- Department Filtering
- Position Filtering

### Recruitment Pipeline

- Track Candidate Progress
- One-Click Stage Updates
- Pipeline Visualization

Pipeline Stages:

```
Applied
↓
Screening
↓
Assessment
↓
Technical
↓
HR
↓
Offer
↓
Accepted
↓
Joined
```

### Interview Management

- Record Interview Feedback
- Ratings
- Strengths and Weaknesses
- Interview Recommendations
- Interview History

### Department Management

- Department CRUD Operations
- Manager Information
- Open Position Tracking

### Analytics Dashboard

- Total Applications
- Interviews Conducted
- Offers Sent
- Offers Accepted
- Offer Acceptance Rate
- Hiring Rate
- Drop-off Rate
- Average Hiring Time

### Reports

- CSV Export
- PDF Export
- Excel Export

---

## Technology Stack

### Frontend

- React
- React Router
- Context API
- Axios
- Tailwind CSS
- Recharts

### Backend

- Node.js
- Express.js
- JWT
- Multer

### Database

- MongoDB Atlas
- Mongoose

### Deployment

- Frontend: Vercel
- Backend: Render
- Database: MongoDB Atlas

---

## System Architecture

```
React Frontend
        │
        ▼
Axios API Requests
        │
        ▼
Express.js Backend
        │
 ┌──────┴──────┐
 │             │
JWT Auth   Business Logic
 │             │
 └──────┬──────┘
        │
        ▼
MongoDB Atlas
```

---

## User Roles

### Admin

- Manage Departments
- Manage Users
- View Dashboard
- Export Reports

### HR Manager

- View Analytics
- View Reports
- Review Interview Feedback
- Compare Department Performance

### Recruiter

- Manage Candidates
- Update Recruitment Stages
- Upload Resumes
- Add Interview Feedback

---

## Database Collections

### Users

| Field | Type |
|--------|------|
| name | String |
| email | String |
| password | String (Hashed) |
| role | String |

### Candidates

| Field | Type |
|--------|------|
| name | String |
| email | String |
| phone | String |
| department | String |
| position | String |
| experience | Number |
| status | String |
| resume | String |
| appliedDate | Date |

### Interviews

| Field | Type |
|--------|------|
| candidateId | ObjectId |
| interviewer | String |
| rating | Number |
| feedback | String |
| round | String |
| result | String |

### Departments

| Field | Type |
|--------|------|
| name | String |
| manager | String |
| openPositions | Number |

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register User |
| POST | /api/auth/login | Login User |
| GET | /api/auth/me | Get Logged-in User |

### Candidates

| Method | Endpoint |
|--------|----------|
| GET | /api/candidates |
| GET | /api/candidates/:id |
| POST | /api/candidates |
| PUT | /api/candidates/:id |
| DELETE | /api/candidates/:id |

### Interviews

| Method | Endpoint |
|--------|----------|
| GET | /api/interviews |
| POST | /api/interviews |
| PUT | /api/interviews/:id |
| DELETE | /api/interviews/:id |

### Departments

| Method | Endpoint |
|--------|----------|
| GET | /api/departments |
| POST | /api/departments |
| PUT | /api/departments/:id |
| DELETE | /api/departments/:id |

### Analytics

| Method | Endpoint |
|--------|----------|
| GET | /api/analytics/kpis |
| GET | /api/analytics/funnel |
| GET | /api/analytics/departments |
| GET | /api/analytics/hiring-time |

---

## Authentication Test Summary

| Test Case | Status |
|-----------|--------|
| User Registration | Passed |
| Duplicate Registration | Passed |
| User Login | Passed |
| Invalid Login | Passed |
| JWT Authentication | Passed |
| Role-Based Authorization | Passed |
| Protected Routes | Passed |

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/hireflow-analytics.git
```

### Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Install Backend Dependencies

```bash
cd backend
npm install
```

### Configure Environment Variables

Create a `.env` file inside the backend directory.

```env
PORT=5000
MONGO_URI=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret
```

### Start Backend

```bash
npm run dev
```

### Start Frontend

```bash
npm run dev
```

---

## Project Structure

```
HireFlow-Analytics/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── context/
│   └── services/
│
├── backend/
│   ├── controllers/
│   ├── middleware/
│   ├── models/
│   ├── routes/
│   ├── uploads/
│   └── server.js
│
├── docs/
│   ├── PRD.md
│   ├── API.md
│   ├── TestCases.md
│   └── ERDiagram.png
│
├── README.md
└── package.json
```

---

## Future Enhancements

- AI-powered interview analysis
- Resume parsing
- Email notifications
- ATS integration
- Candidate recommendation engine
- Predictive hiring analytics
- Real-time dashboard updates

---

## Team

| Name | Responsibility |
|------|----------------|
| Ranjan | Frontend Development and Dashboard |
| Aditya Kannur | Backend Development and API Design |
| Karishma | Database Design, Quality Assurance, Testing, and Documentation |

---

## License

This project was developed as part of an academic software engineering project and is intended for educational purposes.
