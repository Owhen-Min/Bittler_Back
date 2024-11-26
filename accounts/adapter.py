from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        try:
            user = super().save_user(request, user, form, commit=False)
            
            from allauth.account.utils import user_field
            
            user_field(user, 'nickname', request.data.get('nickname'))
            user_field(user, 'first_name', request.data.get('firstname'))
            
            if commit:
                user.save()
            return user
            
        except Exception as e:
            raise e