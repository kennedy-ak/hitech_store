# HiTech Clan Technology Solutions - E-Commerce Platform

![HiTech Clan Logo](https://img.shields.io/badge/HiTech%20Clan-Technology%20Solutions-blue?style=for-the-badge&logo=microchip)

Ghana's premier technology and innovation company's e-commerce platform for hardware solutions and technology services.

## 🏢 About HiTech Clan Technology Solutions

HiTech Clan Technology Solutions Limited is a technology and innovation company based in Ghana, West Africa. We employ the power of technology to improve the lives of our clients and customers in a secure and safe environment.

### Our Services
- 🏠 **Smart Home Systems** - Building automation and integration
- 💻 **Software Development** - Custom software solutions
- 🛡️ **Cybersecurity** - Penetration testing and security services
- 📊 **Data Analysis** - Business intelligence and insights
- 📋 **ICT Project Management** - Professional project services
- ⚖️ **ICT Regulation Consultancy** - Compliance and regulation expertise

## 🚀 Features

### E-Commerce Platform
- **Product Management** - Complete catalog with categories and inventory
- **Shopping Cart** - Session-based and user-specific cart functionality
- **User Authentication** - Registration, login, and profile management
- **Payment Integration** - Paystack payment gateway for secure transactions
- **Order Management** - Complete order tracking and history
- **Responsive Design** - Mobile-friendly interface

### User Profile System
- **Personal Information** - Edit profile with picture upload
- **Shipping Addresses** - Multiple address management with default selection
- **Order History** - Track all purchases and payment status
- **Quick Checkout** - Use saved addresses for faster checkout

### Security Features
- **Environment Variables** - Secure configuration management
- **CSRF Protection** - Cross-site request forgery protection
- **XSS Protection** - Cross-site scripting prevention
- **HTTPS Ready** - SSL/TLS configuration for production

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4 (Python)
- **Frontend**: Bootstrap 5.1.3, HTML5, CSS3, JavaScript
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Payment**: Paystack Payment Gateway
- **Authentication**: Django built-in authentication
- **Security**: python-decouple for environment management

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hitech_store
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
# Update the following required fields:
# - SECRET_KEY (generate a new Django secret key)
# - PAYSTACK_PUBLIC_KEY (your Paystack public key)
# - PAYSTACK_SECRET_KEY (your Paystack secret key)
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure the following:

#### Required Settings
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
PAYSTACK_PUBLIC_KEY=your-paystack-public-key
PAYSTACK_SECRET_KEY=your-paystack-secret-key
```

#### Optional Settings
```env
# Database (for PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=hitech_store
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Payment Setup

1. **Create Paystack Account**:
   - Visit [Paystack](https://paystack.com/)
   - Sign up for an account
   - Get your API keys from the dashboard

2. **Configure Payment**:
   - Add your Paystack keys to `.env` file
   - Test with test keys first
   - Switch to live keys for production

## 📁 Project Structure

```
hitech_store/
├── hitech_store/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Main settings (uses .env)
│   ├── urls.py
│   └── wsgi.py
├── store/
│   ├── migrations/
│   ├── templates/
│   │   ├── registration/    # Auth templates
│   │   └── store/          # Main templates
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py            # Django forms
│   ├── models.py           # Database models
│   ├── urls.py             # URL patterns
│   └── views.py            # View functions
├── static/
│   └── store/
│       ├── css/            # Stylesheets
│       └── js/             # JavaScript files
├── media/                  # User uploads
├── .env                    # Environment variables (not in git)
├── .env.example           # Environment template
├── .gitignore
├── requirements.txt
└── README.md
```

## 🗃️ Database Models

### Core Models
- **Product** - Product catalog with inventory
- **CartItem** - Shopping cart functionality
- **Order** - Order management and tracking
- **OrderItem** - Individual order line items

### User Management
- **UserProfile** - Extended user information
- **ShippingAddress** - User shipping addresses

## 🔐 Security

### Environment Protection
- All sensitive data stored in `.env` file
- `.env` file excluded from version control
- Secure defaults for production settings

### Production Security
- HTTPS enforcement
- Secure cookie settings
- HSTS headers
- XSS protection
- CSRF protection

## 🐳 Docker Deployment

### Prerequisites for Docker
- Docker Engine 20.10+ and Docker Compose 2.0+
- At least 2GB RAM and 10GB disk space

### Quick Start with Docker

#### 1. Development Environment
```bash
# Clone repository
git clone <repository-url>
cd hitech_store

# Copy environment file
cp .env.example .env

# Edit .env with your settings
nano .env

# Build and start services
docker-compose up --build

# Access application at http://localhost
```

#### 2. Production Environment
```bash
# Copy production environment
cp .env.example .env.production

# Configure production settings in .env.production
nano .env.production

# Start production stack
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Docker Services

#### Development Stack (`docker-compose.yml`)
- **web** - Django application (development server)
- **db** - PostgreSQL 15 database
- **redis** - Redis cache server
- **nginx** - Nginx reverse proxy

#### Production Stack (`docker-compose.prod.yml`)
- **web** - Django application (Gunicorn)
- **db** - PostgreSQL with health checks
- **redis** - Redis with persistence
- **nginx** - Nginx with SSL and security headers
- **celery** - Background task worker
- **celery-beat** - Scheduled task scheduler

### Environment Configuration for Docker

#### Required Environment Variables
```env
# Django Core
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=hitech_store
DB_USER=hitech_user
DB_PASSWORD=secure-database-password

# Payment Gateway
PAYSTACK_PUBLIC_KEY=pk_live_your_public_key
PAYSTACK_SECRET_KEY=sk_live_your_secret_key

# Email (Production)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Superuser (Auto-created)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@hitechclan.com
DJANGO_SUPERUSER_PASSWORD=secure-admin-password
```

### Docker Commands

#### Development
```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f web

# Execute commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build
```

#### Production
```bash
# Start production environment
docker-compose -f docker-compose.prod.yml up -d

# Scale web workers
docker-compose -f docker-compose.prod.yml up -d --scale web=3

# View service status
docker-compose -f docker-compose.prod.yml ps

# Update application
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --build

# Backup database
docker-compose -f docker-compose.prod.yml exec db pg_dump -U hitech_user hitech_store > backup.sql

# Restore database
docker-compose -f docker-compose.prod.yml exec -T db psql -U hitech_user hitech_store < backup.sql
```

### SSL Configuration

#### 1. Generate SSL Certificates
```bash
# Create SSL directory
mkdir -p docker/ssl

# Generate self-signed certificate (development)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout docker/ssl/key.pem \
    -out docker/ssl/cert.pem \
    -subj "/C=GH/ST=Ghana/L=Accra/O=HiTech Clan/OU=IT/CN=hitechclan.com"

# For production, use Let's Encrypt or purchased certificates
```

#### 2. Let's Encrypt Integration
```bash
# Using Certbot in Docker
docker run -it --rm --name certbot \
    -v "$(pwd)/docker/ssl:/etc/letsencrypt" \
    -v "$(pwd)/docker/ssl/www:/var/www/certbot" \
    certbot/certbot certonly --webroot \
    -w /var/www/certbot \
    -d hitechclan.com \
    -d www.hitechclan.com
```

### Monitoring and Maintenance

#### Health Checks
```bash
# Check service health
docker-compose -f docker-compose.prod.yml ps

# Check application health
curl -f http://localhost/health

# Check specific services
docker-compose -f docker-compose.prod.yml exec web python manage.py check
```

#### Logging
```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs

# Follow specific service logs
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f nginx

# Export logs
docker-compose -f docker-compose.prod.yml logs > production.log
```

#### Performance Optimization
```bash
# Monitor resource usage
docker stats

# Scale services based on load
docker-compose -f docker-compose.prod.yml up -d --scale web=3 --scale celery=2

# Optimize database
docker-compose -f docker-compose.prod.yml exec db psql -U hitech_user -d hitech_store -c "VACUUM ANALYZE;"
```

### Backup and Recovery

#### Database Backup
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U hitech_user hitech_store > "backup_${DATE}.sql"
gzip "backup_${DATE}.sql"
# Upload to cloud storage
aws s3 cp "backup_${DATE}.sql.gz" s3://hitech-backups/
```

#### Media Files Backup
```bash
# Backup media files
docker run --rm \
    -v hitech_store_media_volume:/source \
    -v $(pwd)/backups:/backup \
    alpine tar czf /backup/media_$(date +%Y%m%d).tar.gz -C /source .
```

### Troubleshooting Docker

#### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :80
   # Change port in docker-compose.yml or stop conflicting service
   ```

2. **Permission denied**
   ```bash
   # Fix ownership
   sudo chown -R $USER:$USER .
   # Or run with sudo
   sudo docker-compose up
   ```

3. **Database connection errors**
   ```bash
   # Check database logs
   docker-compose logs db
   # Ensure database is ready
   docker-compose exec db pg_isready -U hitech_user
   ```

4. **Static files not loading**
   ```bash
   # Collect static files
   docker-compose exec web python manage.py collectstatic --noinput
   # Check Nginx configuration
   docker-compose exec nginx nginx -t
   ```

### 🚀 Traditional Deployment

### Production Checklist

1. **Environment**:
   ```bash
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Database**:
   - Use PostgreSQL for production
   - Configure database backup strategy

3. **Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Security**:
   - Generate new SECRET_KEY
   - Use HTTPS
   - Configure proper ALLOWED_HOSTS

### Recommended Hosting
- **Docker**: Containerized deployment (recommended)
- **Heroku** - Easy deployment with PostgreSQL
- **DigitalOcean** - VPS with Docker support
- **AWS** - Scalable cloud hosting with ECS
- **Railway** - Modern deployment platform

## 🔄 API Integration

### Paystack Integration
- Payment initialization
- Payment verification
- Webhook handling
- Transaction management

## 📱 Frontend Features

### Responsive Design
- Mobile-first approach
- Bootstrap 5 components
- Custom CSS animations
- Interactive JavaScript features

### User Experience
- Smooth animations
- Loading states
- Form validation
- Notification system

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Test Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is proprietary software owned by HiTech Clan Technology Solutions Limited.

## 📞 Support

### Contact Information
- **Company**: HiTech Clan Technology Solutions Limited
- **Email**: info@hitechclan.com
- **Phone**: +233 000 000 000
- **Location**: Ghana, West Africa

### Getting Help
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed description
4. Contact support for urgent matters

## 🔧 Troubleshooting

### Common Issues

#### 1. ImportError: No module named 'decouple'
```bash
pip install python-decouple
```

#### 2. Payment initialization failed
- Check Paystack API keys in `.env`
- Verify account currency settings
- Test with Paystack test keys first

#### 3. Static files not loading
```bash
python manage.py collectstatic
```

#### 4. Database errors
```bash
python manage.py makemigrations
python manage.py migrate
```

### Debug Mode
For development issues, ensure `DEBUG=True` in `.env` file.

## 📈 Performance

### Optimization Tips
- Use PostgreSQL for production
- Configure caching (Redis/Memcached)
- Optimize static file serving
- Use CDN for media files
- Enable gzip compression

## 🔄 Updates

### Keeping Updated
```bash
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
```

## 📊 Monitoring

### Production Monitoring
- Set up logging
- Monitor error rates
- Track performance metrics
- Monitor payment transactions

---

**Built with ❤️ by HiTech Clan Technology Solutions Limited**

*Empowering Ghana with technology solutions since 2020*