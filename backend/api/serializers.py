from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MenuItem, Category, WikiPage, WikiSection, MediaFile, RecentUpdate, SiteSettings, ChatConversation, ChatMessage, UserProfile


class MenuItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'icon', 'menu_type', 'link', 'parent', 'order', 'is_active', 'color', 'children']

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return MenuItemSerializer(children, many=True).data


class WikiSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WikiSection
        fields = ['id', 'title', 'slug', 'content', 'icon', 'icon_color', 'order', 'is_active']
        extra_kwargs = {
            'slug': {'required': False, 'allow_blank': True},
            'content': {'required': False, 'allow_blank': True},
        }


class WikiPageSerializer(serializers.ModelSerializer):
    sections = WikiSectionSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    # Mantener compatibilidad con department_name
    department_name = serializers.CharField(source='category.name', read_only=True)
    department_slug = serializers.CharField(source='category.slug', read_only=True)

    class Meta:
        model = WikiPage
        fields = [
            'id', 'title', 'slug', 'category', 'category_name', 'category_slug',
            'department_name', 'department_slug',  # Compatibilidad
            'heading', 'description', 'content',
            'banner_icon', 'banner_text', 'banner_gradient', 'banner_image',
            'help_text', 'help_button_text',
            'icon', 'is_published', 'is_featured', 'views_count',
            'sections', 'created_at', 'updated_at'
        ]


class WikiPageListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    department_name = serializers.CharField(source='category.name', read_only=True)  # Compatibilidad

    class Meta:
        model = WikiPage
        fields = ['id', 'title', 'slug', 'icon', 'category', 'category_name', 'department_name', 'is_published', 'updated_at']


class WikiPageCreateUpdateSerializer(serializers.ModelSerializer):
    sections = WikiSectionSerializer(many=True, required=False)
    # Aceptar tanto 'category' como 'department' para compatibilidad
    department = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        required=False, 
        write_only=True
    )

    class Meta:
        model = WikiPage
        fields = [
            'id', 'title', 'slug', 'category', 'department',
            'heading', 'description', 'content',
            'banner_icon', 'banner_text', 'banner_gradient', 'banner_image',
            'help_text', 'help_button_text',
            'icon', 'is_published', 'is_featured',
            'sections'
        ]
        extra_kwargs = {
            'category': {'required': False}
        }

    def create(self, validated_data):
        from django.utils.text import slugify
        
        sections_data = validated_data.pop('sections', [])
        # Soportar tanto 'department' como 'category'
        if 'department' in validated_data and 'category' not in validated_data:
            validated_data['category'] = validated_data.pop('department')
        elif 'department' in validated_data:
            validated_data.pop('department')
        
        page = WikiPage.objects.create(**validated_data)
        
        for idx, section_data in enumerate(sections_data):
            # Generar slug si está vacío
            if not section_data.get('slug'):
                title = section_data.get('title', f'section-{idx}')
                section_data['slug'] = slugify(title) or f'section-{idx}'
            
            # Asegurar que content tenga un valor por defecto
            if not section_data.get('content'):
                section_data['content'] = ''
            
            section_data.pop('id', None)  # Remover id si existe
            WikiSection.objects.create(page=page, **section_data)
        
        return page

    def update(self, instance, validated_data):
        from django.utils.text import slugify
        
        sections_data = validated_data.pop('sections', None)
        # Soportar tanto 'department' como 'category'
        if 'department' in validated_data:
            if 'category' not in validated_data:
                validated_data['category'] = validated_data.pop('department')
            else:
                validated_data.pop('department')
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if sections_data is not None:
            existing_ids = []
            for idx, section_data in enumerate(sections_data):
                section_id = section_data.get('id')
                
                # Generar slug si está vacío
                if not section_data.get('slug'):
                    title = section_data.get('title', f'section-{idx}')
                    section_data['slug'] = slugify(title) or f'section-{idx}'
                
                # Asegurar que content tenga un valor por defecto
                if not section_data.get('content'):
                    section_data['content'] = ''
                
                section = None
                
                # Primero intentar buscar por ID
                if section_id:
                    try:
                        section = WikiSection.objects.get(id=section_id, page=instance)
                    except WikiSection.DoesNotExist:
                        section = None
                
                # Si no se encontró por ID, buscar por slug para evitar duplicados
                if section is None:
                    slug = section_data.get('slug')
                    if slug:
                        section = WikiSection.objects.filter(page=instance, slug=slug).first()
                
                if section:
                    # Actualizar sección existente
                    for attr, value in section_data.items():
                        if attr != 'id':
                            setattr(section, attr, value)
                    section.save()
                    existing_ids.append(section.id)
                else:
                    # Crear nueva sección solo si no existe
                    section_data.pop('id', None)
                    # Asegurar slug único agregando sufijo si es necesario
                    base_slug = section_data.get('slug')
                    counter = 1
                    while WikiSection.objects.filter(page=instance, slug=section_data['slug']).exists():
                        section_data['slug'] = f"{base_slug}-{counter}"
                        counter += 1
                    new_section = WikiSection.objects.create(page=instance, **section_data)
                    existing_ids.append(new_section.id)
            
            # Eliminar secciones que ya no están en los datos enviados
            WikiSection.objects.filter(page=instance).exclude(id__in=existing_ids).delete()
        
        return instance


# Serializer recursivo para subcategorías
class SubcategorySerializer(serializers.ModelSerializer):
    pages_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color', 'order', 'is_active', 'pages_count']

    def get_pages_count(self, obj):
        return obj.pages.filter(is_published=True).count()


class CategorySerializer(serializers.ModelSerializer):
    pages = WikiPageListSerializer(many=True, read_only=True)
    pages_count = serializers.SerializerMethodField()
    subcategories = SubcategorySerializer(many=True, read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color', 'order', 'is_active', 
                  'parent', 'parent_name', 'subcategories', 'pages', 'pages_count']
        read_only_fields = ['pages', 'pages_count', 'subcategories']

    def get_pages_count(self, obj):
        return obj.pages.filter(is_published=True).count()


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color', 'order', 'is_active', 'parent']
        extra_kwargs = {
            'slug': {'required': False, 'allow_blank': True},
        }


class CategoryListSerializer(serializers.ModelSerializer):
    pages_count = serializers.SerializerMethodField()
    subcategories_count = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color', 'order', 'is_active', 
                  'parent', 'parent_name', 'pages_count', 'subcategories_count']

    def get_pages_count(self, obj):
        return obj.pages.filter(is_published=True).count()
    
    def get_subcategories_count(self, obj):
        return obj.subcategories.filter(is_active=True).count()


# Alias para compatibilidad
DepartmentSerializer = CategorySerializer
DepartmentListSerializer = CategoryListSerializer
DepartmentCreateUpdateSerializer = CategoryCreateUpdateSerializer


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['id', 'name', 'file_url', 'file_type', 'alt_text', 'size', 'uploaded_at']


class RecentUpdateSerializer(serializers.ModelSerializer):
    page_slug = serializers.CharField(source='page.slug', read_only=True)

    class Meta:
        model = RecentUpdate
        fields = ['id', 'title', 'description', 'icon', 'icon_color', 'link', 'page', 'page_slug', 'created_at']


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ['id', 'site_name', 'site_description', 'welcome_title', 'welcome_message', 'logo_url']


# Dashboard data serializer
class DashboardSerializer(serializers.Serializer):
    categories = CategoryListSerializer(many=True)
    recent_updates = RecentUpdateSerializer(many=True)
    settings = SiteSettingsSerializer()


# Chat serializers
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'sources', 'created_at']


class ChatConversationSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatConversation
        fields = ['id', 'session_id', 'messages', 'created_at', 'updated_at']


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, max_length=2000)
    session_id = serializers.CharField(required=False, max_length=100)


class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    sources = serializers.ListField(child=serializers.DictField())
    session_id = serializers.CharField()
    error = serializers.BooleanField(default=False)


# ============================================================
# Authentication Serializers
# ============================================================

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role', 'avatar_url', 'department', 'is_admin']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    role = serializers.CharField(source='profile.role', read_only=True)
    is_admin = serializers.BooleanField(source='profile.is_admin', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'profile', 'role', 'is_admin']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()
