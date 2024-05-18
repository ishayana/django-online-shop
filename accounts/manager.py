from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    
    def create_user(self, email, phone, full_name, password, **extra_fields):
        if not email:
            raise ValueError('User must have email!')
        
        if not phone:
            raise ValueError('User must have Phone-number!')
        
        if not full_name:
            raise ValueError('Please enter the fullname!')

        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, phone, full_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is False:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is False:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, phone, full_name, password, **extra_fields)