from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models as db_models
from .models import MenuItem, Category, WikiPage, WikiSection, MediaFile, RecentUpdate, SiteSettings, ChatConversation, ChatMessage, UserProfile
from .serializers import (
    MenuItemSerializer,
    CategorySerializer, 
    CategoryListSerializer,
    CategoryCreateUpdateSerializer,
    WikiPageSerializer, 
    WikiPageListSerializer,
    WikiPageCreateUpdateSerializer,
    WikiSectionSerializer,
    MediaFileSerializer,
    RecentUpdateSerializer,
    SiteSettingsSerializer,
    ChatRequestSerializer,
    ChatResponseSerializer,
    ChatMessageSerializer,
    UserSerializer,
    LoginSerializer
)
import uuid


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.filter(parent__isnull=True, is_active=True)
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        queryset = MenuItem.objects.filter(is_active=True)
        menu_type = self.request.query_params.get('type')
        if menu_type:
            queryset = queryset.filter(menu_type=menu_type)
        parent = self.request.query_params.get('parent')
        if parent:
            queryset = queryset.filter(parent_id=parent)
        else:
            queryset = queryset.filter(parent__isnull=True)
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('order', 'name')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return CategoryCreateUpdateSerializer
        return CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all().order_by('order', 'name')
        
        # Filtrar por categoría padre
        parent = self.request.query_params.get('parent')
        if parent == 'null' or parent == '':
            queryset = queryset.filter(parent__isnull=True)
        elif parent:
            queryset = queryset.filter(parent_id=parent)
        
        if self.action == 'list':
            if not self.request.query_params.get('all'):
                queryset = queryset.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        slug = serializer.validated_data.get('slug')
        if not slug:
            name = serializer.validated_data.get('name', '')
            serializer.save(slug=slugify(name))
        else:
            serializer.save()
    
    def perform_update(self, serializer):
        slug = serializer.validated_data.get('slug')
        if not slug:
            name = serializer.validated_data.get('name', '')
            serializer.save(slug=slugify(name))
        else:
            serializer.save()


# Alias para compatibilidad - mantener endpoint /departments/
class DepartmentViewSet(CategoryViewSet):
    pass


class WikiPageViewSet(viewsets.ModelViewSet):
    queryset = WikiPage.objects.all()
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return WikiPageListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return WikiPageCreateUpdateSerializer
        return WikiPageSerializer

    def get_queryset(self):
        queryset = WikiPage.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Compatibilidad con 'department'
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(category__slug=department)
        
        if self.action == 'list' and not self.request.query_params.get('all'):
            queryset = queryset.filter(is_published=True)
        
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if not serializer.validated_data.get('slug'):
            title = serializer.validated_data.get('title', '')
            serializer.save(slug=slugify(title))
        else:
            serializer.save()
        
        page = serializer.instance
        RecentUpdate.objects.create(
            title=page.title,
            description=f"Nueva página creada en {page.category.name}",
            icon=page.icon,
            page=page
        )


class WikiSectionViewSet(viewsets.ModelViewSet):
    queryset = WikiSection.objects.all()
    serializer_class = WikiSectionSerializer

    def get_queryset(self):
        queryset = WikiSection.objects.all()
        page = self.request.query_params.get('page')
        if page:
            queryset = queryset.filter(page__slug=page)
        return queryset

    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        sections_data = request.data.get('sections', [])
        updated = []
        for section_data in sections_data:
            section_id = section_data.get('id')
            if section_id:
                try:
                    section = WikiSection.objects.get(id=section_id)
                    for attr, value in section_data.items():
                        if attr != 'id':
                            setattr(section, attr, value)
                    section.save()
                    updated.append(section_id)
                except WikiSection.DoesNotExist:
                    pass
        return Response({'updated': updated})


class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer

    def get_queryset(self):
        queryset = MediaFile.objects.all()
        file_type = self.request.query_params.get('type')
        if file_type:
            queryset = queryset.filter(file_type=file_type)
        return queryset.order_by('-uploaded_at')


class RecentUpdateViewSet(viewsets.ModelViewSet):
    queryset = RecentUpdate.objects.all()[:20]
    serializer_class = RecentUpdateSerializer


class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

    def get_object(self):
        obj, created = SiteSettings.objects.get_or_create(pk=1)
        return obj

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@api_view(['GET'])
def api_root(request):
    return Response({
        'status': 'ok',
        'message': 'EWiki API v1.0',
        'endpoints': {
            'menu': '/api/menu/',
            'categories': '/api/categories/',
            'departments': '/api/departments/',  # Alias para compatibilidad
            'pages': '/api/pages/',
            'sections': '/api/sections/',
            'media': '/api/media/',
            'updates': '/api/updates/',
            'settings': '/api/settings/',
            'dashboard': '/api/dashboard/',
            'admin_stats': '/api/admin/stats/',
        }
    })


@api_view(['GET'])
def dashboard_data(request):
    """Get all data needed for the dashboard"""
    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by('order', 'name')[:6]
    recent_updates = RecentUpdate.objects.all().order_by('-created_at')[:5]
    settings, _ = SiteSettings.objects.get_or_create(pk=1)
    
    return Response({
        'categories': CategoryListSerializer(categories, many=True).data,
        'departments': CategoryListSerializer(categories, many=True).data,  # Compatibilidad
        'recent_updates': RecentUpdateSerializer(recent_updates, many=True).data,
        'settings': SiteSettingsSerializer(settings).data
    })


@api_view(['GET'])
def admin_stats(request):
    """Get statistics for admin dashboard"""
    return Response({
        'total_categories': Category.objects.count(),
        'active_categories': Category.objects.filter(is_active=True).count(),
        'total_departments': Category.objects.filter(parent__isnull=True).count(),  # Compatibilidad
        'active_departments': Category.objects.filter(is_active=True, parent__isnull=True).count(),
        'total_pages': WikiPage.objects.count(),
        'published_pages': WikiPage.objects.filter(is_published=True).count(),
        'draft_pages': WikiPage.objects.filter(is_published=False).count(),
        'total_sections': WikiSection.objects.count(),
        'total_media': MediaFile.objects.count(),
        'total_views': sum(WikiPage.objects.values_list('views_count', flat=True)),
    })


@api_view(['GET'])
def sidebar_menu(request):
    """Get menu structure for sidebar with categories and subcategories"""
    # Solo categorías principales (sin padre)
    categories = Category.objects.filter(
        is_active=True, 
        parent__isnull=True
    ).prefetch_related('pages', 'subcategories').order_by('order', 'name')
    
    menu_data = []
    for cat in categories:
        cat_data = {
            'id': cat.id,
            'name': cat.name,
            'slug': cat.slug,
            'icon': cat.icon,
            'color': cat.color,
            'order': cat.order,
            'pages': [
                {
                    'id': page.id,
                    'title': page.title,
                    'slug': page.slug,
                    'icon': page.icon
                }
                for page in cat.pages.filter(is_published=True).order_by('title')
            ],
            'subcategories': []
        }
        
        # Agregar subcategorías
        for subcat in cat.subcategories.filter(is_active=True).order_by('order', 'name'):
            subcat_data = {
                'id': subcat.id,
                'name': subcat.name,
                'slug': subcat.slug,
                'icon': subcat.icon,
                'color': subcat.color,
                'order': subcat.order,
                'pages': [
                    {
                        'id': page.id,
                        'title': page.title,
                        'slug': page.slug,
                        'icon': page.icon
                    }
                    for page in subcat.pages.filter(is_published=True).order_by('title')
                ]
            }
            cat_data['subcategories'].append(subcat_data)
        
        menu_data.append(cat_data)
    
    return Response(menu_data)


@api_view(['GET'])
def search_view(request):
    """
    Búsqueda global en páginas y categorías
    """
    query = request.query_params.get('q', '').strip()
    
    if not query or len(query) < 2:
        return Response({
            'pages': [],
            'categories': [],
            'total': 0
        })
    
    # Buscar en páginas
    pages = WikiPage.objects.filter(
        is_published=True
    ).filter(
        db_models.Q(title__icontains=query) |
        db_models.Q(heading__icontains=query) |
        db_models.Q(description__icontains=query) |
        db_models.Q(content__icontains=query)
    ).select_related('category')[:10]
    
    pages_data = [{
        'id': p.id,
        'title': p.title,
        'slug': p.slug,
        'icon': p.icon,
        'description': p.description[:100] + '...' if p.description and len(p.description) > 100 else p.description,
        'category_name': p.category.name if p.category else None,
        'type': 'page'
    } for p in pages]
    
    # Buscar en categorías
    categories = Category.objects.filter(
        is_active=True
    ).filter(
        db_models.Q(name__icontains=query) |
        db_models.Q(description__icontains=query)
    )[:5]
    
    categories_data = [{
        'id': c.id,
        'name': c.name,
        'slug': c.slug,
        'icon': c.icon,
        'color': c.color,
        'description': c.description[:100] + '...' if c.description and len(c.description) > 100 else c.description,
        'type': 'category'
    } for c in categories]
    
    # Buscar en secciones de páginas
    sections = WikiSection.objects.filter(
        is_active=True,
        page__is_published=True
    ).filter(
        db_models.Q(title__icontains=query) |
        db_models.Q(content__icontains=query)
    ).select_related('page')[:5]
    
    sections_data = [{
        'id': s.id,
        'title': s.title,
        'page_title': s.page.title,
        'page_slug': s.page.slug,
        'slug': s.slug,
        'icon': s.page.icon,
        'type': 'section'
    } for s in sections]
    
    return Response({
        'pages': pages_data,
        'categories': categories_data,
        'sections': sections_data,
        'total': len(pages_data) + len(categories_data) + len(sections_data)
    })


@api_view(['GET'])
def categories_tree(request):
    """Get full category tree for admin forms"""
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    
    result = []
    for cat in categories.filter(parent__isnull=True):
        cat_data = {
            'id': cat.id,
            'name': cat.name,
            'slug': cat.slug,
            'children': []
        }
        for subcat in categories.filter(parent=cat):
            cat_data['children'].append({
                'id': subcat.id,
                'name': f"  └─ {subcat.name}",
                'slug': subcat.slug
            })
        result.append(cat_data)
    
    return Response(result)


# ============================================================
# CHAT / RAG ENDPOINTS
# ============================================================

@api_view(['POST'])
def chat_message(request):
    """
    Procesa un mensaje del usuario y retorna una respuesta basada en la Wiki
    """
    serializer = ChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    message = serializer.validated_data['message']
    session_id = serializer.validated_data.get('session_id') or str(uuid.uuid4())
    
    # Obtener o crear conversación
    conversation, created = ChatConversation.objects.get_or_create(session_id=session_id)
    
    # Guardar mensaje del usuario
    ChatMessage.objects.create(
        conversation=conversation,
        role='user',
        content=message
    )
    
    # Obtener historial de conversación
    history = list(conversation.messages.order_by('-created_at')[:10].values('role', 'content'))
    history.reverse()
    
    # Procesar con RAG
    try:
        from .services.rag_service import get_rag_service
        rag = get_rag_service()
        result = rag.chat(message, history)
    except Exception as e:
        import traceback
        traceback.print_exc()
        result = {
            'response': 'Lo siento, el servicio de chat no está disponible en este momento.',
            'sources': [],
            'error': True
        }
    
    # Guardar respuesta del asistente
    ChatMessage.objects.create(
        conversation=conversation,
        role='assistant',
        content=result['response'],
        sources=result.get('sources', [])
    )
    
    return Response({
        'response': result['response'],
        'sources': result.get('sources', []),
        'session_id': session_id,
        'error': result.get('error', False)
    })


@api_view(['GET'])
def chat_history(request):
    """Obtiene el historial de chat de una sesión"""
    session_id = request.query_params.get('session_id')
    
    if not session_id:
        return Response({'messages': []})
    
    try:
        conversation = ChatConversation.objects.get(session_id=session_id)
        messages = ChatMessageSerializer(conversation.messages.all(), many=True).data
        return Response({'messages': messages})
    except ChatConversation.DoesNotExist:
        return Response({'messages': []})


@api_view(['POST'])
def chat_index(request):
    """Re-indexa todo el contenido de la Wiki para el chat"""
    try:
        from .services.rag_service import get_rag_service
        rag = get_rag_service()
        indexed = rag.index_all_pages()
        return Response({
            'success': True,
            'indexed_pages': indexed
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)


@api_view(['GET'])
def chat_stats(request):
    """Obtiene estadísticas del servicio de chat"""
    try:
        from .services.rag_service import get_rag_service
        rag = get_rag_service()
        stats = rag.get_stats()
        return Response(stats)
    except Exception as e:
        return Response({
            'enabled': False,
            'error': str(e)
        })


# ============================================================
# AUTHENTICATION ENDPOINTS
# ============================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Inicio de sesión con email y contraseña
    Retorna tokens JWT y datos del usuario
    """
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    # Buscar usuario por email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            'error': 'Credenciales inválidas',
            'detail': 'El email o la contraseña son incorrectos'
        }, status=401)
    
    # Autenticar
    user = authenticate(username=user.username, password=password)
    
    if user is None:
        return Response({
            'error': 'Credenciales inválidas',
            'detail': 'El email o la contraseña son incorrectos'
        }, status=401)
    
    if not user.is_active:
        return Response({
            'error': 'Cuenta desactivada',
            'detail': 'Tu cuenta ha sido desactivada. Contacta al administrador.'
        }, status=403)
    
    # Asegurar que existe el perfil
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': 'admin' if user.is_superuser else 'reader'}
    )
    
    # Generar tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """Refresca el token de acceso"""
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        return Response({
            'error': 'Token requerido',
            'detail': 'El refresh token es requerido'
        }, status=400)
    
    try:
        refresh = RefreshToken(refresh_token)
        return Response({
            'access': str(refresh.access_token),
        })
    except Exception as e:
        return Response({
            'error': 'Token inválido',
            'detail': 'El refresh token es inválido o ha expirado'
        }, status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """Obtiene los datos del usuario autenticado"""
    # Asegurar que existe el perfil
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'admin' if request.user.is_superuser else 'reader'}
    )
    
    return Response(UserSerializer(request.user).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Invalida el refresh token (logout)"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Sesión cerrada correctamente'})
    except Exception:
        return Response({'message': 'Sesión cerrada'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_admin(request):
    """Verifica si el usuario tiene permisos de administrador"""
    try:
        is_admin = request.user.profile.is_admin or request.user.is_superuser
    except UserProfile.DoesNotExist:
        is_admin = request.user.is_superuser
    
    return Response({
        'is_admin': is_admin,
        'user_id': request.user.id,
        'email': request.user.email
    })
