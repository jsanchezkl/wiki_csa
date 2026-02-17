from django.db import models
from django.contrib.auth.models import User


class MenuItem(models.Model):
    """Elementos del menú principal"""
    MENU_TYPES = [
        ('main', 'Main Menu'),
        ('category', 'Category'),
    ]
    
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='folder')
    menu_type = models.CharField(max_length=20, choices=MENU_TYPES, default='main')
    link = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    color = models.CharField(max_length=50, default='blue')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']


class Category(models.Model):
    """Categorías del Wiki (antes Departments) - soporta subcategorías"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='folder')
    color = models.CharField(max_length=50, default='blue')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Relación para subcategorías
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    @property
    def full_path(self):
        """Retorna la ruta completa de la categoría"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name


class WikiPage(models.Model):
    """Páginas del Wiki"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pages')
    
    # Contenido principal
    heading = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True, help_text="Contenido HTML del editor")
    
    # Banner
    banner_icon = models.CharField(max_length=50, default='description')
    banner_text = models.CharField(max_length=200, blank=True)
    banner_gradient = models.CharField(max_length=100, default='bg-gradient-to-br from-blue-500 to-primary')
    banner_image = models.URLField(blank=True, null=True)
    
    # Sidebar
    help_text = models.CharField(max_length=300, blank=True)
    help_button_text = models.CharField(max_length=100, default='Contact Support')
    
    # Metadatos
    icon = models.CharField(max_length=50, default='description')
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']


class WikiSection(models.Model):
    """Secciones dentro de una página Wiki"""
    page = models.ForeignKey(WikiPage, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField(help_text="Contenido HTML de la sección")
    icon = models.CharField(max_length=50, blank=True)
    icon_color = models.CharField(max_length=50, default='primary')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.page.title} - {self.title}"

    class Meta:
        ordering = ['order']
        unique_together = ['page', 'slug']


class MediaFile(models.Model):
    """Archivos multimedia para el Wiki"""
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
    ]
    
    name = models.CharField(max_length=200)
    file_url = models.URLField()
    file_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default='image')
    alt_text = models.CharField(max_length=300, blank=True)
    size = models.PositiveIntegerField(default=0, help_text="Size in bytes")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RecentUpdate(models.Model):
    """Actualizaciones recientes para mostrar en el dashboard"""
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    icon = models.CharField(max_length=50, default='description')
    icon_color = models.CharField(max_length=50, default='primary')
    link = models.CharField(max_length=200, blank=True)
    page = models.ForeignKey(WikiPage, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class SiteSettings(models.Model):
    """Configuración general del sitio"""
    site_name = models.CharField(max_length=100, default='EWiki')
    site_description = models.TextField(blank=True)
    welcome_title = models.CharField(max_length=200, default='Welcome back!')
    welcome_message = models.TextField(blank=True)
    logo_url = models.CharField(max_length=500, blank=True)  # Permite URLs y rutas relativas
    
    class Meta:
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name


class ChatConversation(models.Model):
    """Conversaciones del chat"""
    session_id = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.session_id}"

    class Meta:
        ordering = ['-updated_at']


class ChatMessage(models.Model):
    """Mensajes del chat"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    sources = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"

    class Meta:
        ordering = ['created_at']


class WikiPageEmbedding(models.Model):
    """
    Embeddings de páginas Wiki para búsqueda semántica (RAG)
    
    Diseñado para fácil migración a PostgreSQL + pgvector:
    - El campo 'embedding' se puede convertir a vector(768) en pgvector
    - Las búsquedas se pueden hacer con operadores nativos (<=> para coseno)
    
    Ejemplo de migración a pgvector:
    ALTER TABLE api_wikipageembedding 
    ALTER COLUMN embedding TYPE vector(768) 
    USING embedding::vector(768);
    
    CREATE INDEX ON api_wikipageembedding 
    USING ivfflat (embedding vector_cosine_ops);
    """
    page = models.OneToOneField(
        WikiPage, 
        on_delete=models.CASCADE, 
        related_name='embedding_data'
    )
    content_text = models.TextField(
        help_text="Texto limpio usado para generar el embedding"
    )
    embedding = models.JSONField(
        default=list,
        help_text="Vector de embedding (768 dimensiones para text-embedding-004)"
    )
    embedding_model = models.CharField(
        max_length=100, 
        default='gemini-embedding-001',
        help_text="Modelo usado para generar el embedding"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Embedding: {self.page.title}"

    class Meta:
        verbose_name = "Wiki Page Embedding"
        verbose_name_plural = "Wiki Page Embeddings"


class UserProfile(models.Model):
    """
    Perfil de usuario con roles
    - reader: Solo puede ver contenido
    - admin: Acceso completo (ver + administrar)
    """
    ROLE_CHOICES = [
        ('reader', 'Lector'),
        ('admin', 'Administrador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')
    avatar_url = models.URLField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.get_role_display()}"

    @property
    def is_admin(self):
        return self.role == 'admin'

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


# Alias para compatibilidad - Department ahora es Category
Department = Category
