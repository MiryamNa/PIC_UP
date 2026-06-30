# PicUp - Intelligent Photo Selection and Filtering Tool

## 📋 Project Overview

**PicUp** is an intelligent photo management system designed to automatically filter, categorize, and select high-quality photos from large event photo repositories. The system helps photographers reduce manual selection time by up to 70% while improving accuracy and maintaining consistent quality.
## My Contributions

## I was responsible for:

- Designing the backend architecture
- Creating MongoDB schemas
- Implementing REST APIs
- Developing image filtering algorithms
- Building React components
- Integrating backend and frontend


### Problem Statement
During large-scale photography events, photographers accumulate thousands of images that require manual sorting and selection. This manual process is:
- Time-consuming (requires 30-40% of total event work)
- Error-prone (risk of missing quality photos or keeping duplicates)
- Labor-intensive for large repositories

### Solution
PicUp automates this workflow through intelligent algorithms that:
- Filter photos by quality metrics (sharpness, contrast, exposure)
- Detect and eliminate duplicate images
- Categorize photos by content and event segments
- Allow precise selection of desired photo quantities
- Organize results for easy review and export


## Data Flow
User Uploads Photos
        ↓
React Frontend
        ↓
FastAPI Backend
        ↓
Image Processing Service
        ↓
OpenCV + PyTorch
        ↓
MongoDB Atlas
        ↓
Processed Results
        ↓
Frontend Display

## 🎯 Key Features

- ✅ **Automatic Photo Filtering** - Quality-based selection (sharpness, contrast, brightness)
- ✅ **Smart Categorization** - AI-powered classification of photos by event segments
- ✅ **Duplicate Detection** - Identify and remove similar/duplicate images
- ✅ **Face Detection** - Automatically identify and highlight bride/groom and key people
- ✅ **Flexible Selection** - Users define exact quantity of photos needed
- ✅ **User-Friendly Interface** - Intuitive React-based GUI for non-technical users
- ✅ **High Scalability** - Process hundreds to thousands of photos simultaneously
- ✅ **Security Features** - JWT authentication, Password hashing, HTTPS/TLS support, File type validation, Input validation

---

## 🛠️ Technology Stack

### Backend
- **Language:** Python 3.x
- **Framework:** FastAPI (for REST API)
- **Image Processing:** OpenCV
- **Machine Learning:** PyTorch
- **Database:** MongoDB with Mongoose ODM

### Frontend

- Framework: React.js
- HTTP Client: Axios
- Styling: CSS (Flexbox, Grid, Media Queries)
- Responsive Design: Mobile and desktop support

### Infrastructure & DevOps
- **Cloud Platform:** AWS (with GPU support for image processing)
- **Database Hosting:** MongoDB Atlas
- **Version Control:** Git & GitHub
- **Deployment:** Docker (containerized)

### Development Tools
- **IDE:** VS Code
- **Package Management:** Python (pip), Node.js (npm)
- **API Testing:** Postman

---

## 📁 Project Structure

```
app_picUp/
├── controllers/              # Request handlers & route controllers
│   ├── category_controller.py
│   ├── customer_controller.py
│   ├── event_controller.py
│   └── ...
├── database/                 # Database connection & configuration
│   └── mongo.py
├── models/                   # Data models & schemas
│   ├── Customer.py
│   ├── Event.py
│   ├── Images.py
│   └── ...
├── services/                 # Business logic & algorithms
│   ├── category_service.py
│   ├── image_uploader.py
│   ├── sharpness.py
│   ├── similar.py            # Duplicate detection
│   ├── people_match.py       # Face detection & matching
│   ├── MachineLearning.py
│   └── ...
├── repository/               # Data access layer
│   ├── customer_repository.py
│   ├── event_repository.py
│   └── ...
├── dto/                      # Data Transfer Objects
│   ├── EventDTO.py
│   ├── imageDTO.py
│   └── ...
├── error_handlers/           # Custom error handling
├── exceptions/               # Custom exception definitions
├── main.py                   # Application entry point
├── db.py                     # Database initialization
└── requirements.txt          # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB (local or Atlas)
- AWS account (for GPU processing)
- Git

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/app_picUp.git
cd app_picUp
```

#### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Environment Configuration
Create a `.env` file in the root directory:
```
MONGODB_URI=your_mongodb_connection_string
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
JWT_SECRET=your_jwt_secret
```

#### 4. Database Setup
```bash
# Run database initialization
python db.py
```

#### 5. Start Backend Server
```bash
python main.py
```
Server runs on: `http://localhost:5000`

#### 6. Frontend Setup (separate terminal)
```bash
cd frontend
npm install
npm start
```
Frontend runs on: `http://localhost:3000`

---

## 📊 System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────┐
│                    React Frontend (GUI)              │
│            - Photo Upload & Preview                  │
│            - Filter Configuration                    │
│            - Results Display & Management            │
└──────────────────────┬──────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────┐
│              Python Backend (FastAPI)         │
│    - Route Controllers                              │
│    - Business Logic & Services                      │
│    - Authentication & Authorization                 │
└──────────────┬──────────────────┬───────────────────┘
               │                  │
        ┌──────▼────┐      ┌──────▼──────┐
        │ MongoDB    │      │ Processing  │
        │ Database   │      │ Engine (GPU)│
        │ - Photos   │      │ - OpenCV    │
        │ - Metadata │      │ - PyTorch   │
        │ - Users    │      │ - Filters   │
        └────────────┘      └─────────────┘
```

### Core Components

| Component | Purpose | Technologies        |
|-----------|---------|---------------------|
| **Photo Upload Module** | Receive & store images | FastAPI, MongoDB    |
| **Filtering Engine** | Quality & content analysis | OpenCV, PyTorch     |
| **Face Detection** | Identify key people | PyTorch|
| **Duplicate Detector** | Find similar images | Vector matching, ML |
| **Categorization Engine** | Auto-classify photos | AI+ML models        |
| **User Interface** | Display & manage results | React.js            |

---

## 🧠 Core Algorithms

### 1. Quality Filtering
Analyzes images for:
- **Sharpness** - Detects blur using Laplacian variance
- **Contrast** - Evaluates image depth and detail
- **Exposure** - Checks brightness levels
- **Composition** - Analyzes layout and framing

### 2. Duplicate Detection
- Converts images to vector embeddings
- Compares similarity using cosine distance
- Targets <5% false positive rate

### 3. Face Detection & Recognition
- Detects faces using PyTorch models
- Identifies bride/groom/key people
- Matches faces across photo collection

### 4. Automatic Categorization
Segments photos into:
- Bride preparation
- Groom preparation
- Ceremony
- Reception
- Special moments
- Candid shots

---

## 📈 Project Goals & Metrics

### Primary Objectives
1. **Reduce Manual Selection Time** - 70% time reduction
2. **Improve Accuracy** - <5% error rate in duplicate detection
3. **Increase Efficiency** - 50% faster photo delivery workflow
4. **User Satisfaction** - Intuitive interface requiring no technical knowledge

### Performance Targets
Target goals:
- Reduce manual selection time
- Improve duplicate detection accuracy
- Accelerate photo delivery workflow
---

## 🔒 Security Features

Security:
- JWT authentication
- Password hashing
- HTTPS support
- File type validation
- Input validation
---

## 🧪 Testing Strategy

### Unit Tests
- Filter algorithm accuracy
- Data persistence functions
- API endpoint validation
- Authentication/authorization

### Integration Tests
- End-to-end photo upload workflow
- Filter pipeline execution
- Database transactions
- API integration

### Load Testing
- Concurrent user handling
- Large photo repository processing
- Database query performance
- GPU resource management

### Security Testing
- Penetration testing
- Vulnerability scanning
- Access control validation
- Data encryption verification

## Technical Challenges

- Handling large photo repositories efficiently
- Reducing duplicate detection false positives
- Optimizing image processing performance
- Managing asynchronous processing workflows
---

## 📚 Dependencies

### Python Packages
```
FastAPI
OpenCV
PyTorch
MongoDB/Pymongo
Pillow
NumPy
Scikit-learn
```

### Node.js Packages
```
React
Axios
React Router
Material-UI or Bootstrap
```

See `requirements.txt` for complete Python dependencies list.

---

## 🤝 Contributing

### Development Workflow
1. Create a feature branch: `git checkout -b feature/feature-name`
2. Commit changes: `git commit -m "Add feature description"`
3. Push to branch: `git push origin feature/feature-name`
4. Open a Pull Request with detailed description

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable/function names
- Add docstrings to functions
- Write unit tests for new features
- Maintain README documentation

---

## 📝 Current Status

**Status:** Active Development (MVP Phase)

### Completed
- [x] Project planning & requirements analysis
- [x] Architecture design
- [x] Database schema design
- [x] Project structure setup

### In Progress
- [ ] Core photo upload module
- [ ] Image quality filtering
- [ ] Face detection implementation
- [ ] Duplicate detection algorithm
- [ ] Frontend UI development

### Planned
- [ ] Machine learning model training
- [ ] Integration testing
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Deployment & documentation

---

## 📄 License

This project is developed as part of Software Engineering graduation requirements at [College Name]. 

---

## 🔗 Additional Resources

### Documentation
- [API Documentation](./docs/API.md) - *Coming soon*
- [User Manual](./docs/USER_MANUAL.md) - *Coming soon*
- [Technical Architecture](./docs/ARCHITECTURE.md) - *Coming soon*
- [Algorithm Details](./docs/ALGORITHMS.md) - *Coming soon*

### External References
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [MongoDB Manual](https://docs.mongodb.com/manual/)
- [React Documentation](https://react.dev/)

---

**Last Updated:** June 17, 2026
**Version:** 0.1.0 (Development)
