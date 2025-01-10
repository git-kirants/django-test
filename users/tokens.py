from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Handle both User and ProviderApplication objects
        if hasattr(user, 'business_name'):  # It's a ProviderApplication
            return (
                str(user.pk) + str(timestamp) + str(user.is_active) + str(user.business_name)
            )
        else:  # It's a User
            return (
                str(user.pk) + str(timestamp) + str(user.is_active)
            )

account_activation_token = EmailVerificationTokenGenerator() 