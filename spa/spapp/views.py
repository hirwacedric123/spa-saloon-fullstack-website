from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import ContactForm, SubscribeForm
from .models import Subscriber,ContactMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.
def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def specialist(request):
    return render(request, 'specialist.html')

@csrf_exempt  # To allow POST requests without CSRF token (for simplicity; use CSRF token in production)
def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['user_email']
            # Save the subscriber's email to the database
            subscriber = Subscriber.objects.create(user_email=user_email)
            # Send subscription confirmation email
            send_email_to_subscriber(user_email)
            # Send subscription notification to admin
            send_subscription_notification('cielomassagespa@gmail.com', user_email)
            return render(request, 'thank_you.html')
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for subscription.'}, status=400)

def send_email_to_subscriber(user_email):
    subject = 'Welcome to Our Newsletter!'
    message = 'Thank you for subscribing to our newsletter. Stay tuned for updates!'
    sender_email = 'cielomassagespa@gmail.com'  # Use your email address
    recipient_list = [user_email]

    send_mail(subject, message, sender_email, recipient_list)

def send_subscription_notification(admin_email, subscriber_email):
    subject = 'New Subscriber Notification'
    message = f'A new user has subscribed to the newsletter.\nSubscriber Email: {subscriber_email}'
    sender_email = 'cielomassagespa@gmail.com'  # Use your email address
    recipient_list = [admin_email]

    send_mail(subject, message, sender_email, recipient_list)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']
            
            # Save form data to the database
            submission = ContactMessage.objects.create(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                message=message
            )
            
            # Send email to admin with message details
            admin_subject = 'New Contact Form Submission'
            admin_message = render_to_string('cf/admin_contact_notification_email.html', {
                'full_name': full_name,
                'email': email,
                'phone_number': phone_number,
                'message': message
            })
            admin_email_text = strip_tags(admin_message)
            admin_email_html = admin_message
            admin_email = EmailMultiAlternatives(admin_subject, admin_email_text, 'cielomassagespa@gmail.com', ['cielomassagespa@gmail.com'])
            admin_email.attach_alternative(admin_email_html, "text/html")
            admin_email.send()
            
            # Send confirmation email to sender
            sender_subject = 'Contact Form Submission Confirmation'
            sender_message = render_to_string('cf/sender_contact_confirmation_email.html', {
                'full_name': full_name
            })
            sender_email_text = strip_tags(sender_message)
            sender_email_html = sender_message
            sender_email = EmailMultiAlternatives(sender_subject, sender_email_text, 'cielomassagespa@gmail.com', [email])
            sender_email.attach_alternative(sender_email_html, "text/html")
            sender_email.send()
            
            # Optionally, you can redirect the user to a thank you page
            return render(request, 'thank_you.html')
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {'form': form})