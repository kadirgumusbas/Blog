from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):

    list_display = ['id','title', 'publishing_date', 'slug']
    list_display_links = ['id','title', 'publishing_date']
    list_filter = ['publishing_date']
    search_fields = ['title', 'content']
    #prepopulated_fields = {'slug': ('title',)} slugun titleı referans alarak dolmasını sağlar
    ordering = ['-id'] #sıralama yapmamızı sağlıyor
    #list_editable = ['title'] direkt başlığın düzenlenmesine izin veriyor

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)