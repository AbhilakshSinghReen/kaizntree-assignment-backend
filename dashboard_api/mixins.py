from django.core.cache import cache


class CacheMixin:
    def generate_primary_cache_key(self, organization_id, other_fields):
        sorted_keys = sorted(other_fields.keys())
        other_fields_str = "--".join([f"{key}-{other_fields[key]}" for key in sorted_keys])
        return f"{organization_id}__{other_fields_str}"
    
    def generate_all_cache_key(self, organization_id):
        return f"{organization_id}__{self.model_name}"
    
    def generate_single_cache_key(self, organization_id, id):
        return f"{organization_id}__{self.model_name}__{id}"
    
    def get_all_cache(self, organization_id):
        all_cache_key = self.generate_all_cache_key(organization_id)
        return cache.get(all_cache_key, None)
    
    def get_single_cache(self, organization_id, id):
        single_cache_key = self.generate_single_cache_key(organization_id, id)
        return cache.get(single_cache_key, None)
    
    def set_all_cache(self, organization_id, data):
        all_cache_key = self.generate_all_cache_key(organization_id)
        cache.set(all_cache_key, data)

    def set_single_cache(self, organization_id, id, data):
        single_cache_key = self.generate_single_cache_key(organization_id, id)
        cache.set(single_cache_key, data)

    def delete_all_cache(self, organization_id):
        all_cache_key = self.generate_all_cache_key(organization_id)
        if all_cache_key in cache:
            cache.delete(all_cache_key)

    def delete_single_cache(self, organization_id, id):
        single_cache_key = self.generate_single_cache_key(organization_id, id)
        if single_cache_key in cache:
            cache.delete(single_cache_key)
