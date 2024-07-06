import yaml

class ConfigManager:
    config_file = 'config.yaml'
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = cls._instance.load_config(cls.config_file)
        return cls._instance

    def load_config(self, file_path):
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def get_from_email(self):
        return self.config.get('email', {}).get('from_email')
    
    def get_from_password(self):
        return self.config.get('email', {}).get('from_password')
    
    def get_to_email(self):
        return self.config.get('email', {}).get('to_email')
    
    def get_base_url(self):
        return self.config.get('url', {}).get('base_url')
    
    def get_user_email(self):
        return self.config.get('eClerx', {}).get('emailId')
    
    def get_user_password(self):
        return self.config.get('eClerx', {}).get('password')

# Example usage:
if __name__ == '__main__':
    config_manager1 = ConfigManager()
    config_manager2 = ConfigManager()  # Creating another instance should return the same instance

    print(f"From Email: {config_manager1.get_from_email()}")
    print(f"From Password: {config_manager1.get_from_password()}")
    print(f"Base URL: {config_manager1.get_base_url()}")

    # Both instances should be the same
    print(f"Are both instances the same? {config_manager1 is config_manager2}")
