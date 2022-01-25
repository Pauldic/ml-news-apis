from allauth.account.signals import user_logged_in, user_logged_out, user_signed_up, password_set, password_changed, password_reset, email_confirmed, email_confirmation_sent, email_changed, email_added, email_removed
from allauth.socialaccount.signals import pre_social_login, social_account_added, social_account_updated, social_account_removed
from django.dispatch import receiver
 
 
@receiver(user_logged_in)
def user_logged_in_(request, user):
    ''' Sent when a user logs in. '''
    print("*** user_logged_in")

@receiver(user_logged_out)
def user_logged_out_(request, user):
    ''' Sent when a user logs out.'''
    print("*** user_logged_out")

@receiver(user_signed_up)
def user_signed_up_(request, user):
    '''
    Sent when a user signs up for an account. This signal is typically followed by a user_logged_in, unless e-mail verification prohibits the user to log in.
    '''
    print("*** user_signed_up")
        
        
@receiver(password_set)
def password_set_(request, user):
    '''
    Sent when a password has been successfully set for the first time.
    '''
    print("*** password_set")
        
          
@receiver(password_changed)
def password_changed_(request, user):
    '''
    Sent when a password has been successfully changed.
    '''
    print("*** password_changed")
        
          
@receiver(password_reset)
def password_reset_(request, user):
    '''
    Sent when a password has been successfully reset.

    '''
    print("*** password_reset")
        
          
@receiver(email_confirmed)
def email_confirmed_(request, email_address):
    ''' Sent after the email address in the db was updated and set to confirmed.'''
    
    # user = User.objects.get(email=email_address.email)
    # user.is_active = True
    # user.save()
    print("*** email_confirmed")

@receiver(email_confirmation_sent)
def email_confirmation_sent_(request, confirmation, signup):
    ''' Sent right after the email confirmation is sent.'''
    
    print("*** email_confirmation_sent")

@receiver(email_changed)
def email_changed_(request, user, from_email_address, to_email_address):
    ''' Sent when a primary email address has been changed.'''
    print("*** email_changed")

@receiver(email_added)
def email_added_(request, user, email_address):
    ''' Sent when a new email address has been added.'''
    print("*** email_added")

@receiver(email_removed)
def email_removed_(request, user, email_address):
    ''' Sent when an email address has been deleted.'''
    print("*** email_removed")
    
@receiver(pre_social_login)
def pre_social_login_(request, sociallogin):
    ''' 
    Sent after a user successfully authenticates via a social provider, 
    but before the login is fully processed. This signal is emitted as 
    part of the social login and/or signup process, as well as when 
    connecting additional social accounts to an existing account. 
    Access tokens and profile information, if applicable for the 
    provider, is provided.'''
    print("*** pre_social_login")
    
@receiver(social_account_added)
def social_account_added_(request, sociallogin):
    ''' Sent after a user connects a social account to a their local account. '''
    print("*** social_account_added")
    
@receiver(social_account_updated)
def social_account_updated_(request, sociallogin):
    ''' 
    Sent after a social account has been updated. This happens 
    when a user logs in using an already connected social account, 
    or completes a connect flow for an already connected social 
    account. Useful if you need to unpack extra data for social 
    accounts as they are updated.
    '''
    print("*** social_account_updated")
    
@receiver(social_account_removed)
def social_account_removed_(request, sociallogin):
    ''' Sent after a user disconnects a social account from their local account.'''
    print("*** social_account_removed")
    