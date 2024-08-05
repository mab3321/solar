from .models import Service

# Define built-in integrations (replace with your actual data)
BUILTIN_INTEGRATIONS = [
    {'name': 'Logos', 'category': 'start', 'resource': 'https://example.com'},
    {'name': 'Internet/Phone services', 'category': 'start', 'resource': 'https://example.com'},
    {'name': 'Domain', 'category': 'start', 'resource': 'https://example.com'},
    {'name': 'Business Banking', 'category': 'start', 'resource': 'https://example.com'},
    {'name': 'Website', 'category': 'start', 'resource': 'https://example.com'},
    {'name': 'Credit Card Processing', 'category': 'manage', 'resource': 'https://example.com'},
    {'name': 'LLC', 'category': 'manage', 'resource': 'https://example.com'},
    {'name': 'EIN', 'category': 'manage', 'resource': 'https://example.com'},
    {'name': 'Taxes and Accounting', 'category': 'manage', 'resource': 'https://example.com'},
    {'name': 'Business Loan/Credit', 'category': 'manage', 'resource': 'https://example.com'},
    {'name': 'Business Insurance', 'category': 'growth', 'resource': 'https://example.com'},
    {'name': 'Attorney', 'category': 'growth', 'resource': 'https://example.com'},
    {'name': 'Print Store', 'category': 'growth', 'resource': 'https://example.com'},
    {'name': 'Restaurant Supplies', 'category': 'growth', 'resource': 'https://example.com'},
    {'name': 'ADP Payroll', 'category': 'growth', 'resource': 'https://example.com'},
        
]


def create_builtin_integrations():
    for integration_data in BUILTIN_INTEGRATIONS:
        Service.objects.get_or_create(
            name=integration_data['name'],
            category=integration_data['category'],
            resource=integration_data['resource'],
            type=True
        )


# You can call this function during application startup (e.g., in your main app file)
# create_builtin_integrations()
