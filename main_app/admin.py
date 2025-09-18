from django.contrib import admin
from .models import Education, EducationAchievement, DiplomaImage, ServiceQuery, ExcludeService


class DiplomaImageInline(admin.TabularInline):
    model = DiplomaImage
    extra = 1
    max_num = 3  # Ограничиваем количество изображений до 3
    fields = ('image', 'order')

class EducationAchievementInline(admin.TabularInline):
    model = EducationAchievement
    extra = 1
    fields = ('title', 'description', 'is_active', 'order')
    inlines = [DiplomaImageInline]

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('year', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    inlines = [EducationAchievementInline]

@admin.register(EducationAchievement)
class EducationAchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'education', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('education', 'is_active')
    inlines = [DiplomaImageInline]
    search_fields = ('title', 'description')



@admin.register(ServiceQuery)
class ServiceQueryAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)


@admin.register(ExcludeService)
class ExcludeServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)

