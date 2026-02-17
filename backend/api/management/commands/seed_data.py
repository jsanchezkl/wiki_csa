from django.core.management.base import BaseCommand
from api.models import Category, WikiPage, WikiSection, RecentUpdate, SiteSettings


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create site settings
        settings, _ = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'CSA Wiki',
                'site_description': 'Wiki Corporativo',
                'welcome_title': 'Bienvenido!',
                'welcome_message': 'Explora nuestra base de conocimiento corporativa.'
            }
        )
        
        # Create HR Category (main)
        hr_cat, _ = Category.objects.get_or_create(
            slug='hr',
            defaults={
                'name': 'Human Resources',
                'description': 'Políticas, beneficios y manual del empleado.',
                'icon': 'groups',
                'color': 'blue',
                'order': 2
            }
        )
        
        # Create other main categories
        categories_data = [
            {'name': 'Tech & Analytics', 'slug': 'tech-analytics', 'icon': 'settings_suggest', 'color': 'indigo', 'description': 'Guías de configuración, acceso a software y soluciones.', 'order': 1},
            {'name': 'Projects', 'slug': 'projects', 'icon': 'tactic', 'color': 'emerald', 'description': 'Metodologías, plantillas y sprints activos.', 'order': 3},
            {'name': 'Legal & Compliance', 'slug': 'legal', 'icon': 'gavel', 'color': 'amber', 'description': 'Contratos, GDPR y estándares de seguridad.', 'order': 4},
            {'name': 'Marketing', 'slug': 'marketing', 'icon': 'campaign', 'color': 'rose', 'description': 'Recursos de marca, guías y campañas.', 'order': 5},
            {'name': 'Finance', 'slug': 'finance', 'icon': 'payments', 'color': 'purple', 'description': 'Gastos, nómina y solicitudes de presupuesto.', 'order': 6},
        ]
        
        for cat_data in categories_data:
            Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
        
        # Create subcategory example inside HR
        policies_subcat, _ = Category.objects.get_or_create(
            slug='hr-policies',
            defaults={
                'name': 'Políticas',
                'description': 'Políticas internas de la empresa',
                'icon': 'policy',
                'color': 'blue',
                'order': 1,
                'parent': hr_cat
            }
        )
        
        benefits_subcat, _ = Category.objects.get_or_create(
            slug='hr-benefits',
            defaults={
                'name': 'Beneficios',
                'description': 'Beneficios para empleados',
                'icon': 'favorite',
                'color': 'blue',
                'order': 2,
                'parent': hr_cat
            }
        )
        
        # Create Policies page
        policies_page, created = WikiPage.objects.get_or_create(
            slug='policies',
            defaults={
                'title': 'Policies & Benefits',
                'category': hr_cat,
                'heading': 'Employee Policies & Benefits',
                'description': 'Guía completa de beneficios para empleados, políticas de la empresa y recursos disponibles.',
                'banner_icon': 'policy',
                'banner_text': 'Tu Guía de Beneficios',
                'banner_gradient': 'bg-gradient-to-br from-blue-500 to-primary',
                'help_text': '¿Preguntas sobre beneficios? Contacta a HR directamente.',
                'help_button_text': 'Contactar HR',
                'icon': 'policy',
            }
        )
        
        if created:
            WikiSection.objects.create(
                page=policies_page,
                title='Health Insurance',
                slug='health-insurance',
                icon='health_and_safety',
                order=1,
                content='''<p class="text-slate-600 dark:text-slate-400 mb-6">Proporcionamos cobertura de salud completa para todos los empleados de tiempo completo desde el primer día.</p>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
<div class="p-5 rounded-2xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800">
<span class="material-symbols-outlined text-primary mb-3">medical_services</span>
<h4 class="font-bold text-slate-900 dark:text-white mb-2">Cobertura Médica</h4>
<p class="text-slate-500 dark:text-slate-400 text-sm">Planes PPO y HDHP disponibles con 90% de prima pagada por el empleador.</p>
</div>
<div class="p-5 rounded-2xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800">
<span class="material-symbols-outlined text-primary mb-3">dentistry</span>
<h4 class="font-bold text-slate-900 dark:text-white mb-2">Dental & Visión</h4>
<p class="text-slate-500 dark:text-slate-400 text-sm">Cobertura dental y de visión completa incluida sin costo adicional.</p>
</div>
</div>'''
            )
            
            WikiSection.objects.create(
                page=policies_page,
                title='Time Off Policy',
                slug='time-off',
                icon='beach_access',
                order=2,
                content='''<p class="text-slate-600 dark:text-slate-400 mb-6">Creemos en el balance trabajo-vida y ofrecemos políticas flexibles de tiempo libre.</p>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
<div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700">
<h4 class="font-bold text-primary mb-2">Tiempo Libre Pagado</h4>
<p class="text-sm text-slate-600 dark:text-slate-400">20 días PTO por año, aumentando con la antigüedad.</p>
</div>
<div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700">
<h4 class="font-bold text-primary mb-2">Licencia por Enfermedad</h4>
<p class="text-sm text-slate-600 dark:text-slate-400">Días de enfermedad ilimitados - tu salud es lo primero.</p>
</div>
</div>'''
            )
        
        # Create Onboarding page
        WikiPage.objects.get_or_create(
            slug='onboarding',
            defaults={
                'title': 'Onboarding',
                'category': hr_cat,
                'heading': 'New Employee Onboarding',
                'description': 'Todo lo que necesitas para comenzar tu primer día y más allá. ¡Bienvenido al equipo!',
                'banner_icon': 'rocket_launch',
                'banner_text': 'Tu Viaje Comienza Aquí',
                'banner_gradient': 'bg-gradient-to-br from-emerald-500 to-teal-600',
                'help_text': '¿Necesitas ayuda con el onboarding? Tu buddy está aquí para asistirte.',
                'help_button_text': 'Contactar Buddy',
                'icon': 'person_add',
            }
        )
        
        # Create Training page
        WikiPage.objects.get_or_create(
            slug='training',
            defaults={
                'title': 'Training',
                'category': hr_cat,
                'heading': 'Training & Development',
                'description': 'Desarrolla tus habilidades con nuestros programas de aprendizaje. Invertimos en tu crecimiento.',
                'banner_icon': 'school',
                'banner_text': 'Nunca Dejes de Aprender',
                'banner_gradient': 'bg-gradient-to-br from-purple-500 to-indigo-600',
                'help_text': 'Tu Progreso: 65% - 3 de 5 cursos completados',
                'help_button_text': 'Ver Todos los Cursos',
                'icon': 'school',
            }
        )
        
        # Create recent updates
        RecentUpdate.objects.get_or_create(
            title='Q3 Strategy Roadmap.pdf',
            defaults={
                'description': 'Actualizado por Sarah J. • hace 2h',
                'icon': 'description',
                'icon_color': 'primary',
                'page': policies_page
            }
        )
        
        self.stdout.write(self.style.SUCCESS('¡Base de datos poblada exitosamente!'))
