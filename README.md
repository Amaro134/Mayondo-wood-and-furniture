# Mayondo Wood and Furniture Management System

<div align="center">
  <img src="Mayondo/static/images/2.png" alt="Mayondo Logo" width="100" height="100">
  
  **A comprehensive inventory and sales management system built with Django**
  
  [![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://djangoproject.com/)
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Contributing](#-contributing)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## 🌟 Overview

Mayondo Wood and Furniture Management System is a modern, secure web application designed to streamline inventory management, sales tracking, and reporting for furniture businesses. Built with Django and featuring a responsive design, it provides comprehensive tools for managing stock, recording sales transactions, handling user roles, and generating detailed reports.

### Key Benefits

- **Streamlined Operations**: Centralized management of inventory and sales
- **Role-Based Access**: Secure authentication with Admin, Manager, and Sales Agent roles
- **Real-Time Reporting**: Comprehensive analytics and reporting capabilities
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Scalable Architecture**: Built to grow with your business needs

## ✨ Features

### 🔐 Authentication & Authorization
- **Secure User Authentication**: JWT-based login system with Django's built-in security
- **Role-Based Access Control**: Three user roles (Admin, Manager, Sales Agent)
- **User Management**: Complete CRUD operations for user accounts
- **Session Management**: Secure session handling with configurable timeouts

### 📦 Inventory Management
- **Product Registration**: Comprehensive product details including specifications
- **Stock Tracking**: Real-time quantity monitoring with low-stock alerts
- **Supplier Management**: Track supplier information and relationships
- **Cost & Pricing**: Manage cost prices and selling prices
- **Quality Control**: Quality specifications and measurements tracking

### 💰 Sales Management
- **Transaction Recording**: Complete sales transaction capture
- **Customer Management**: Customer information and purchase history
- **Payment Tracking**: Multiple payment methods (Cash, Cheque, Bank Transfer)
- **Transport Coordination**: Company or self-provision transport options
- **Receipt Generation**: Professional sales receipts and invoices
- **Sales Agent Assignment**: Track sales performance by agent

### 📊 Reporting & Analytics
- **Dashboard Overview**: Executive summary with key metrics
- **Sales Reports**: Detailed sales analytics with date ranges
- **Inventory Reports**: Stock levels, values, and movement analysis
- **Summary Reports**: Combined sales and inventory insights
- **Export Capabilities**: PDF and Excel export options

### 🎨 User Interface
- **Modern Design**: Clean, professional interface using Tailwind CSS
- **Responsive Layout**: Optimized for all device sizes
- **Intuitive Navigation**: User-friendly sidebar navigation
- **Interactive Elements**: Hover effects, transitions, and visual feedback
- **Accessibility**: WCAG-compliant design principles

## 🛠 Technologies Used

### Backend
- **Framework**: Django 5.2.6
- **Language**: Python 3.8+
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: Django's built-in authentication system
- **Security**: CSRF protection, XSS filtering, secure sessions

### Frontend
- **CSS Framework**: Tailwind CSS 3.x
- **Icons**: Boxicons
- **JavaScript**: Vanilla JS for interactivity
- **Template Engine**: Django Templates

### Development & Deployment
- **Environment Management**: python-decouple
- **Static Files**: WhiteNoise
- **Image Handling**: Pillow
- **Version Control**: Git

## 📁 Project Structure

```
Mayondo-wood-and-furniture/
├── 📄 README.md                    # Project documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 .gitignore                  # Git ignore file
├── 📄 .env.example                # Environment variables template
├── 📄 PROJECT_ANALYSIS.md         # Detailed project analysis
│
├── 📁 Mayondo/                     # Main Django project
│   ├── 📁 Mayondo/                 # Project configuration
│   │   ├── ⚙️ settings.py          # Django settings
│   │   ├── 🌐 urls.py              # URL routing
│   │   ├── 🚀 wsgi.py              # WSGI configuration
│   │   └── 🔄 asgi.py              # ASGI configuration
│   │
│   ├── 📁 authentication/          # Authentication app
│   │   ├── 👁️ views.py             # Authentication views
│   │   ├── 🌐 urls.py              # Authentication URLs
│   │   └── 📱 apps.py              # App configuration
│   │
│   ├── 📁 Wood/                    # Main business logic app
│   │   ├── 🗃️ models.py            # Database models
│   │   ├── 👁️ views.py             # Business logic views
│   │   ├── 📝 forms.py             # Django forms
│   │   ├── ⚙️ admin.py             # Admin configuration
│   │   └── 🔄 migrations/          # Database migrations
│   │
│   ├── 📁 templates/               # HTML templates
│   │   ├── 📁 authentication/      # Auth templates
│   │   ├── 📁 inventory/           # Stock templates
│   │   ├── 📁 sales/              # Sales templates
│   │   ├── 📁 users/              # User management templates
│   │   ├── 📁 reports/            # Reporting templates
│   │   └── 🏠 base.html            # Base template
│   │
│   ├── 📁 static/                  # Static files
│   │   └── 📁 images/             # Images and assets
│   │
│   ├── 📁 logs/                    # Application logs
│   ├── 🗄️ db.sqlite3               # Database file
│   └── ⚙️ manage.py                # Django management script
```

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/mayondo-wood-furniture.git
   cd mayondo-wood-furniture
   ```

2. **Create Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv mayondo_env
   
   # Activate virtual environment
   # On Windows:
   mayondo_env\Scripts\activate
   
   # On macOS/Linux:
   source mayondo_env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env file with your settings (optional for development)
   # For development, default values will work
   ```

5. **Navigate to Project Directory**
   ```bash
   cd Mayondo
   ```

6. **Database Setup**
   ```bash
   # Apply database migrations
   python manage.py migrate
   
   # Create superuser (optional)
   python manage.py createsuperuser
   ```

7. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

9. **Access the Application**
   - **Main Application**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Security Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Allowed Hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (Production)
DATABASE_URL=postgresql://user:password@localhost:5432/mayondo_db

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Production Deployment

For production deployment, ensure:

1. **Set `DEBUG=False`** in your environment variables
2. **Configure proper database** (PostgreSQL recommended)
3. **Set up proper `ALLOWED_HOSTS`**
4. **Configure static files serving**
5. **Set up SSL/HTTPS**
6. **Configure logging and monitoring**

## 📖 Usage

### Getting Started

1. **Access the Landing Page**
   - Navigate to the application URL
   - Choose to either sign in or register

2. **User Registration**
   - Click \"Register\" on the landing page
   - Fill in username, email, role, and password
   - Select appropriate role (Admin, Manager, Sales Agent)

3. **Login**
   - Use your credentials to sign in
   - You'll be redirected to the dashboard

### Dashboard Overview

The dashboard provides:
- **Quick Stats**: Total stock, current stock, revenue
- **Recent Activity**: Latest sales and stock entries
- **Navigation**: Access to all system features

### Managing Inventory

1. **Adding Stock**
   - Navigate to Inventory → Add Stock
   - Fill in product details, pricing, and supplier information
   - Submit to add to inventory

2. **Viewing Stock**
   - Go to Inventory → Stock List
   - View all products with quantities and pricing
   - Use search and filter options

3. **Editing Stock**
   - Click edit icon on any stock item
   - Update information and save changes

### Recording Sales

1. **New Sale**
   - Navigate to Sales → Add Sale
   - Select customer and product information
   - Specify payment method and transport
   - System calculates total automatically

2. **Sales Management**
   - View all sales in Sales → Sales List
   - Edit, delete, or view individual transactions
   - Generate receipts for customers

### User Management

(Admin/Manager only)
- **Add Users**: Create new user accounts
- **Manage Roles**: Assign appropriate access levels
- **User Profile**: View and edit user information

### Generating Reports

1. **Sales Reports**
   - Access Reports → Sales Report
   - View detailed sales analytics
   - Export data for external analysis

2. **Inventory Reports**
   - Check Reports → Stock Report
   - Monitor stock levels and values
   - Identify low-stock items

3. **Summary Reports**
   - View Reports → Summary Report
   - Get combined business insights
   - Track overall performance

## 🌐 API Endpoints

### Authentication URLs
```
/                          # Landing page
/login/                    # User login
/register/                 # User registration
/logout/                   # User logout
/profile/                  # User profile
```

### Inventory URLs
```
/inventory/add/            # Add new stock
/inventory/list/           # List all stock
/inventory/<id>/edit/      # Edit stock item
/inventory/<id>/view/      # View stock details
/inventory/<id>/delete/    # Delete stock item
```

### Sales URLs
```
/sales/add/                # Add new sale
/sales/list/               # List all sales
/sales/<id>/edit/          # Edit sale
/sales/<id>/view/          # View sale details
/sales/<id>/delete/        # Delete sale
/sales/<id>/receipt/       # Generate receipt
```

### User Management URLs
```
/users/list/               # List all users
/users/add/                # Add new user
/users/<id>/edit/          # Edit user
/users/<id>/view/          # View user profile
/users/<id>/delete/        # Delete user
```

### Reports URLs
```
/reports/                  # Reports dashboard
/reports/sales/            # Sales report
/reports/stock/            # Stock report
/reports/summary/          # Summary report
```

## 🤝 Contributing

We welcome contributions to improve the Mayondo Wood and Furniture Management System!

### How to Contribute

1. **Fork the Repository**
   ```bash
   git fork https://github.com/yourusername/mayondo-wood-furniture.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Commit Changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```

5. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open Pull Request**
   - Describe your changes
   - Include screenshots if UI changes
   - Reference any related issues

### Development Guidelines

- **Code Style**: Follow PEP 8 for Python code
- **Testing**: Add tests for new features
- **Documentation**: Update README and docstrings
- **Security**: Follow Django security best practices

## 🔒 Security

### Security Features

- **CSRF Protection**: Built-in Django CSRF protection
- **XSS Prevention**: Automatic output escaping
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **Secure Sessions**: Httponly and secure cookie flags
- **Password Security**: Django's built-in password hashing

### Security Best Practices

1. **Keep Dependencies Updated**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Regular Security Audits**
   ```bash
   pip install safety
   safety check
   ```

3. **Environment Security**
   - Never commit sensitive data
   - Use environment variables for secrets
   - Implement proper access controls

### Reporting Security Issues

If you discover a security vulnerability, please email security@mayondo.com instead of opening a public issue.

## 🔧 Troubleshooting

### Common Issues

#### Import Error: No module named 'django'
```bash
# Ensure virtual environment is activated
source mayondo_env/bin/activate  # Linux/Mac
# or
mayondo_env\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt
```

#### Database Migration Issues
```bash
# Reset migrations (development only)
python manage.py migrate --fake-initial

# Create new migration
python manage.py makemigrations
python manage.py migrate
```

#### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_URL and STATIC_ROOT settings
```

#### Authentication Issues
```bash
# Create superuser
python manage.py createsuperuser

# Check user permissions in admin panel
```

### Getting Help

- **Documentation**: Check this README and code comments
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact support@mayondo.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Team**: For the excellent web framework
- **Tailwind CSS**: For the utility-first CSS framework
- **Boxicons**: For the beautiful icons
- **Contributors**: All developers who have contributed to this project

## 📞 Contact

- **Developer**: Amarorwot Naomi
- **Email**: naomi@mayondo.com
- **Project Link**: https://github.com/yourusername/mayondo-wood-furniture

---

<div align="center">
  <p>Made with ❤️ for the furniture industry</p>
  <p>© 2025 Mayondo Wood and Furniture. All rights reserved.</p>
</div>