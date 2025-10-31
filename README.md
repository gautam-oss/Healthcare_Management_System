# 🏥 Healthcare Management System

A comprehensive full-stack healthcare platform that connects patients and doctors, featuring appointment booking, AI-powered health assistance, ML-based insurance cost prediction, and streamlined healthcare management. Built with Django and powered by Google's Gemini AI. Currently deployed temporarily on Render 🚀

![Django](https://img.shields.io/badge/Django-5.2.6-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Machine Learning](https://img.shields.io/badge/ML-Insurance_Prediction-orange)

## 📸 Screenshots

### 🏠 Homepage - Hero Section
![Homepage](https://postimg.cc/bGGQMd3V)

*Modern landing page featuring:*
- **Gradient Hero Design**: Eye-catching purple gradient background
- **Clear Value Proposition**: "Your Health, Our Priority"
- **Dual CTAs**: Get Started Free & Login buttons
- **Trust Indicators**: No Credit Card Required, 100% Secure badges
- **Fully Responsive**: Mobile-first design approach

---

### ⚡ Powerful Features Section
![Features Overview](https://i.postimg.cc/yJJF5WLV/Screenshot-2025-10-31-191654.png)

*Showcasing four core features:*

| Feature | Description | Access |
|---------|-------------|--------|
| 📅 **Book Appointments** | Schedule consultations with qualified doctors instantly | Login Required |
| 🤖 **AI Health Assistant** | Get instant health advice powered by Gemini AI | Public Access ✅ |
| 💰 **Insurance Calculator** | Predict insurance costs using ML algorithms | Public Access ✅ |
| 📋 **Health Records** | Track appointments and prediction history | Login Required |

---

### 🤖 AI Health Assistant - Chat Interface
![AI Chatbot](https://i.postimg.cc/94vGjVkW/Screenshot-2025-10-31-191728.png)

*Intelligent health companion powered by Google Gemini AI:*

**✨ Key Capabilities:**
- 💬 Real-time conversational AI responses
- 🏥 General health information and tips
- 💊 Medication information (general, non-prescription)
- 🩺 Symptom guidance (not diagnosis)
- 📚 Understanding medical terminology
- 🏃 Healthy lifestyle recommendations
- ⏰ Available 24/7 for health queries

**🎨 Interface Features:**
- Clean, modern chat bubbles
- Typing indicators for better UX
- Message timestamps
- Quick question suggestions
- Guest mode with optional registration
- Conversation history (for logged-in users)

**⚠️ Important Note:** Always consult healthcare professionals for medical advice

---

### 💰 Insurance Cost Predictor - ML Form
![Insurance Predictor](https://i.postimg.cc/CZWjVY2S/Screenshot-2025-10-31-191756.png)

*AI-powered insurance cost estimation using Linear Regression:*

**📋 Input Parameters:**
1. **Age** (18-100 years) - Impact: ~$257 per year
2. **Sex** (Male/Female) - Impact: ~$131 difference
3. **BMI** (Body Mass Index) - Impact: ~$339 per BMI point
4. **Number of Children** (0-10) - Impact: ~$475 per child
5. **Smoker Status** (Yes/No) - Impact: ~$23,848 increase ⚠️
6. **Region** (NE/NW/SE/SW) - Impact: Regional variation

**🎯 Model Benefits:**
- ⚡ Instant predictions using trained ML model
- 📊 Feature importance visualization
- ⚠️ Risk factor identification
- 💡 Personalized health recommendations
- 📈 Prediction history tracking (registered users)
- 📉 Cost statistics and trends

**🔬 Technical Details:**
- **Algorithm**: Linear Regression
- **Training Data**: Industry-standard insurance datasets
- **Accuracy**: Real-time predictions with <1s latency
- **Transparency**: Full feature importance breakdown

---

## 🎨 Design Highlights

### Color Scheme
- **Primary:** Purple gradient (#667eea → #764ba2)
- **Success:** Green (#10B981)
- **Warning:** Amber (#F59E0B)
- **Info:** Blue (#3B82F6)
- **Danger:** Red (#EF4444)

### UI/UX Features
- ✨ **Glassmorphism** - Modern frosted glass effects
- 🎭 **Smooth Animations** - Fade-in, slide-in, hover effects
- 📱 **Fully Responsive** - Mobile-first design approach
- 🎯 **Accessibility** - WCAG compliant components
- 🌓 **Dark Mode Ready** - CSS variables for easy theming

---

## ✨ Features

### 👥 **User Management**
- **Dual User Types**: Separate registration and dashboards for patients and doctors
- **Secure Authentication**: Django's built-in authentication with custom user model
- **Profile Management**: Comprehensive profiles with medical information

### 📅 **Appointment System**
- **Easy Booking**: Patients can book appointments with available doctors
- **Real-time Status Updates**: Track appointment status (Pending, Confirmed, Completed, Cancelled)
- **Doctor Management**: Doctors can manage and update appointment statuses
- **Appointment History**: Complete history with timestamps and notes

### 🤖 **AI-Powered Health Assistant**
- **Gemini AI Integration**: Advanced conversational AI for health guidance
- **Health Information**: Get reliable medical information and explanations
- **Symptom Guidance**: AI assistance for understanding symptoms (not a replacement for medical advice)
- **Conversation History**: Persistent chat history for continued conversations

### 💰 **ML-Based Insurance Cost Predictor**
- **Linear Regression Model**: Trained machine learning model for accurate cost predictions
- **Multiple Factors Analysis**: Considers age, sex, BMI, children, smoking status, and region
- **Risk Assessment**: Identifies key risk factors and provides personalized recommendations
- **Feature Importance Visualization**: Understand which factors most impact insurance costs
- **Prediction History**: Track and compare multiple predictions over time
- **Cost Statistics**: View average, minimum, and maximum predicted costs
- **Interactive Dashboard**: Beautiful UI with charts and progress bars

### 🎨 **Modern UI/UX**
- **Responsive Design**: Bootstrap 5 for mobile-first design
- **Interactive Elements**: Real-time chat interface with typing indicators
- **Professional Healthcare Theme**: Clean, medical-focused design
- **Accessibility**: WCAG compliant interface elements

## 🛠 Tech Stack

### **Backend**
- **Django 5.2.6**: Web framework
- **PostgreSQL**: Primary database
- **Google Gemini AI**: Conversational AI service
- **Scikit-learn**: Machine learning model (Linear Regression)
- **Django REST Framework**: API development (ready for extension)

### **Frontend**
- **HTML5/CSS3**: Structure and styling
- **Bootstrap 5**: Responsive UI framework
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Icon library

### **Machine Learning**
- **Linear Regression**: Insurance cost prediction model
- **NumPy**: Numerical computations
- **Pickle**: Model serialization

### **DevOps & Deployment**
- **Docker & Docker Compose**: Containerization
- **Gunicorn**: WSGI HTTP Server
- **Nginx**: Reverse proxy and static file serving
- **PostgreSQL**: Production database

### **Development Tools**
- **python-decouple**: Environment variable management
- **Django Debug Toolbar**: Development debugging (optional)
- **Whitenoise**: Static file serving

## 📁 Project Structure

```
Healthcare_Management_System/
├── Healthcare_Management_System/     # Main project configuration
│   ├── __init__.py
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # Main URL configuration
│   ├── wsgi.py                       # WSGI configuration
│   └── asgi.py                       # ASGI configuration
├── users/                            # User management app
│   ├── models.py                     # User, Patient, Doctor models
│   ├── views.py                      # Authentication views
│   ├── forms.py                      # Registration forms
│   ├── admin.py                      # Admin configuration
│   └── templates/users/              # User templates
├── appointments/                     # Appointment management app
│   ├── models.py                     # Appointment model
│   ├── views.py                      # Appointment CRUD views
│   ├── forms.py                      # Appointment forms
│   └── templates/appointments/       # Appointment templates
├── chatbot/                          # AI chatbot app
│   ├── models.py                     # Conversation & Message models
│   ├── views.py                      # Chat API views
│   ├── services.py                   # Gemini AI integration
│   └── templates/chatbot/            # Chat interface
├── insurance/                        # Insurance prediction app
│   ├── models.py                     # InsurancePrediction model
│   ├── views.py                      # Prediction views
│   ├── forms.py                      # Prediction forms
│   ├── ml_model.py                   # Linear Regression model
│   ├── trained_model.pkl             # Serialized ML model
│   ├── admin.py                      # Admin configuration
│   └── templates/insurance/          # Insurance templates
├── static/                           # Static files
│   ├── css/
│   └── js/
├── templates/                        # Global templates
│   ├── base.html                     # Base template
│   └── navbar.html                   # Navigation component
├── screenshots/                      # Application screenshots
│   ├── homepage-hero.png
│   ├── features-overview.png
│   ├── ai-chatbot.png
│   ├── insurance-predictor.png
│   └── ...
├── requirements.txt                  # Python dependencies
├── manage.py                         # Django management script
├── Dockerfile                        # Docker configuration
├── docker-compose.yml               # Docker Compose setup
└── README.md                         # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11+ 
- PostgreSQL 15+
- Docker & Docker Compose (for containerized deployment)
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/gautam-oss/Healthcare-Management-System.git
   cd Healthcare-Management-System
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   # Create PostgreSQL database
   createdb healthcare_db
   
   # Run migrations
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

   Visit: `http://localhost:8000`

### Docker Deployment

1. **Clone and navigate to project**
   ```bash
   git clone https://github.com/gautam-oss/Healthcare-Management-System.git
   cd Healthcare-Management-System
   ```

2. **Create production environment file**
   ```bash
   cp .env.example .env.production
   # Edit .env.production with production values
   ```

3. **Build and run with Docker Compose**
   ```bash
   # Development
   docker-compose up --build
   
   # Production
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

4. **Run migrations in container**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**
   - Application: `http://localhost:8000`
   - Admin Panel: `http://localhost:8000/admin`

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Django Configuration
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration  
DB_NAME=healthcare_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Security Settings (Production)
SECURE_SSL_REDIRECT=False
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
```

### Gemini API Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the API key to your `.env` file as `GEMINI_API_KEY`

### Production Settings

For production deployment, ensure:
- `DEBUG=False`
- Configure `ALLOWED_HOSTS` with your domain
- Use HTTPS and enable security headers
- Set up proper database backups
- Configure logging and monitoring

## 🎯 Usage

### For Patients

1. **Register**: Create a patient account with personal and medical information
2. **Login**: Access your personalized dashboard
3. **Book Appointments**: 
   - Browse available doctors
   - Select preferred date and time
   - Provide reason for visit
4. **AI Health Assistant**: 
   - Ask health-related questions
   - Get symptom guidance
   - Receive medication information
5. **Insurance Cost Prediction**:
   - Enter personal health information (age, BMI, smoking status, etc.)
   - Get instant ML-powered cost predictions
   - View risk factors and recommendations
   - Track prediction history with statistics
6. **Manage Appointments**: View and track appointment status

### For Doctors

1. **Register**: Create a doctor account with professional credentials
2. **Login**: Access doctor dashboard with patient management tools
3. **Manage Appointments**:
   - View incoming appointment requests
   - Confirm or reschedule appointments
   - Add clinical notes
   - Update appointment status
4. **AI Assistant**: Use AI for patient education and information
5. **Insurance Insights**: Access insurance prediction tool for patient cost estimates

### Admin Features

- User management (patients and doctors)
- Appointment oversight and management
- Insurance prediction history and analytics
- System configuration and monitoring
- AI conversation logs and analytics

## 🔧 API Documentation

### Authentication Endpoints
- `POST /users/login/` - User login
- `POST /users/logout/` - User logout
- `POST /users/register/patient/` - Patient registration
- `POST /users/register/doctor/` - Doctor registration

### Appointment Endpoints
- `GET /appointments/my/` - List user appointments
- `POST /appointments/book/` - Create new appointment
- `PUT /appointments/update/{id}/` - Update appointment (doctors only)

### Chatbot Endpoints
- `GET /chatbot/` - Chat interface
- `POST /chatbot/send/` - Send message to AI

### Insurance Endpoints
- `GET /insurance/predict/` - Insurance prediction form
- `POST /insurance/predict/` - Submit prediction data
- `GET /insurance/result/<id>/` - View prediction result
- `GET /insurance/history/` - View prediction history
- `GET /insurance/about/` - Model information and feature importance

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test appointments
python manage.py test chatbot
python manage.py test insurance

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🤖 Machine Learning Model Details

### Insurance Cost Predictor

**Model Type**: Linear Regression

**Features Analyzed**:
1. **Smoking Status** (Highest Impact): Smokers pay significantly higher premiums (~$23,848 increase)
2. **BMI**: Higher BMI correlates with increased costs (~$339 per BMI point)
3. **Age**: Older individuals typically have higher insurance costs (~$257 per year)
4. **Number of Children**: More dependents increase coverage costs (~$475 per child)
5. **Region**: Geographic location affects pricing (varies by region)
6. **Sex**: Minor impact on insurance costs (~$131 difference)

**Model Performance**:
- Pre-trained coefficients based on industry-standard insurance datasets
- Accurate predictions for annual health insurance costs
- Feature importance visualization for transparency
- Risk factor identification and personalized recommendations

**Technical Implementation**:
- Pickle serialization for model persistence
- NumPy for efficient numerical computations
- Real-time prediction with minimal latency
- Extensible architecture for model updates

## 🔒 Security Features

- **CSRF Protection**: Django's built-in CSRF middleware
- **XSS Prevention**: Template auto-escaping and security headers
- **SQL Injection Prevention**: Django ORM parameterized queries
- **Secure Password Hashing**: Django's PBKDF2 algorithm
- **Session Security**: Secure session management
- **Input Validation**: Form validation and sanitization
- **User Data Privacy**: Prediction history tied to authenticated users

## 📈 Performance Optimization

- **Database Indexing**: Optimized database queries
- **Static File Compression**: Gzip compression for static files
- **Caching**: Redis caching for frequently accessed data (ready for implementation)
- **Database Connection Pooling**: Persistent database connections
- **ML Model Caching**: Pre-loaded model for instant predictions

## 🚀 Deployment Options

### 1. Traditional VPS/Server
- Use Gunicorn + Nginx
- PostgreSQL database
- SSL/TLS configuration

### 2. Docker Containerization
- Multi-stage Docker builds
- Docker Compose for orchestration
- Environment-based configuration

### 3. Cloud Platforms
- **Heroku**: Ready for Heroku deployment
- **AWS**: ECS/EKS compatible
- **Google Cloud**: Cloud Run ready
- **DigitalOcean**: App Platform compatible
- **Render**: Currently deployed (temporary)

## 🛡️ Production Checklist

Before deploying to production:

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Set up HTTPS/SSL
- [ ] Configure database backups
- [ ] Set up monitoring and logging
- [ ] Run security checklist: `python manage.py check --deploy`
- [ ] Configure error tracking (Sentry recommended)
- [ ] Set up CI/CD pipeline
- [ ] Performance testing completed
- [ ] ML model validation and testing

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages
- Test ML model predictions thoroughly

## 🐛 Issue Reporting

Found a bug? Please report it:

1. Check existing issues first
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information
   - Screenshots (if applicable)

## 📞 Support

For support and questions:
- **Documentation**: Check this README first
- **Issues**: [GitHub Issues](https://github.com/gautam-oss/Healthcare-Management-System/issues)
- **Email**: gautamkumarxpvt@gmail.com
- **LinkedIn**: [Gautam Kumar](https://www.linkedin.com/in/gautam-kumar-4b6475255/)

## 🗺️ Roadmap

### Completed Features ✅
- [x] User authentication (Patient & Doctor)
- [x] Appointment booking system
- [x] AI Health Assistant (Gemini AI)
- [x] Insurance Cost Prediction (ML)
- [x] Responsive UI/UX
- [x] Docker deployment
- [x] Admin panel

### Upcoming Features 🚀
- [ ] **Mobile App**: React Native mobile application
- [ ] **Video Consultations**: Integrated video calling
- [ ] **Payment Integration**: Stripe/PayPal payment processing
- [ ] **Electronic Health Records**: Complete EHR system
- [ ] **Prescription Management**: Digital prescription system
- [ ] **Multi-language Support**: Internationalization
- [ ] **Advanced Analytics**: Healthcare analytics dashboard
- [ ] **API v2**: RESTful API for third-party integrations
- [ ] **Email Notifications**: Automated appointment reminders
- [ ] **SMS Notifications**: Twilio integration

### Future Enhancements 🔮
- Enhanced ML models (Neural Networks, XGBoost)
- Disease prediction using ML
- Medication interaction checker
- Wearable device integration (Fitbit, Apple Watch)
- Telemedicine platform expansion
- Healthcare data analytics and insights
- Real-time insurance quote comparison
- Voice assistant integration
- Blockchain for medical records
- Integration with pharmacy systems

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Gautam Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- **Django Community**: For the excellent web framework
- **Google AI**: For Gemini AI API access
- **Bootstrap Team**: For the responsive UI framework
- **PostgreSQL**: For the robust database system
- **Font Awesome**: For the beautiful icons
- **Scikit-learn**: For machine learning capabilities
- **NumPy**: For numerical computing support
- **Open Source Community**: For countless libraries and tools

## 🌟 Star History

If you find this project helpful, please consider giving it a ⭐ on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=gautam-oss/Healthcare-Management-System&type=Date)](https://star-history.com/#gautam-oss/Healthcare-Management-System&Date)

---

## 💡 Quick Start Commands

```bash
# Clone and setup
git clone https://github.com/gautam-oss/Healthcare-Management-System.git
cd Healthcare-Management-System
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Database setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Or with Docker
docker-compose up --build
```

**🎉 You're ready to revolutionize healthcare management with AI and ML!**

---

## 📊 Project Statistics

- **Total Lines of Code**: ~15,000+
- **Python Files**: 50+
- **HTML Templates**: 20+
- **CSS/JS Files**: 5+
- **Database Models**: 8
- **API Endpoints**: 15+
- **Test Cases**: 30+ (expandable)
- **Dependencies**: 20+

---

<p align="center">
  <strong>Made with ❤️ by <a href="https://github.com/gautam-oss">Gautam Kumar</a></strong>
</p>

<p align="center">
  <a href="https://github.com/gautam-oss">GitHub</a> •
  <a href="https://www.linkedin.com/in/gautam-kumar-4b6475255/">LinkedIn</a> •
  <a href="https://www.instagram.com/gautam.pratap.singh/">Instagram</a>
</p>

<p align="center">
  <a href="#top">⬆️ Back to Top</a>
</p>


[url=https://postimg.cc/bGGQMd3V][img]https://i.postimg.cc/bGGQMd3V/Screenshot-2025-10-31-191639.png[/img][/url]

[url=https://postimg.cc/yJJF5WLV][img]https://i.postimg.cc/yJJF5WLV/Screenshot-2025-10-31-191654.png[/img][/url]

[url=https://postimg.cc/94vGjVkW][img]https://i.postimg.cc/94vGjVkW/Screenshot-2025-10-31-191728.png[/img][/url]

[url=https://postimg.cc/CZWjVY2S][img]https://i.postimg.cc/CZWjVY2S/Screenshot-2025-10-31-191756.png[/img][/url]

