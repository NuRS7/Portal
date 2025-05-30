from django.contrib import admin
from .models import Zhukteme
import openpyxl
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.http import HttpResponseRedirect
from django.contrib import admin
from .models import *

admin.site.register(Kyrs)
admin.site.register(Toby)
admin.site.register(Oky_tury)
admin.site.register(Dareje)
admin.site.register(Kyzmet)
admin.site.register(CustomUser)
admin.site.register(Sabak_teacher_toby)
admin.site.register(Sabak)
admin.site.register(Grade)
admin.site.register(Toby_kurator)
admin.site.register(Sabak_turu)
admin.site.register(Sabak_lek)
admin.site.register(Week)

@admin.register(Zhukteme)
class ZhuktemeAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'lectures', 'practices', 'tests', 'rate', 'zhalaqy', 'total_load', 'adjusted_load')
    actions = ['export_as_excel', 'go_to_public_page']


    def export_as_excel(self, request, queryset):
        from openpyxl import Workbook

        wb = Workbook()
        ws = wb.active
        ws.title = "Жүктеме"


        headers = ['Оқытушы', 'Лекциялар саны', 'Практикалар саны', 'Тестер', 'Мөлшерлеме (ставка)', 'Жалақы']
        ws.append(headers)


        for obj in queryset:
            ws.append([
                obj.teacher.get_full_name(),
                obj.lectures,
                obj.practices,
                obj.tests,
                float(obj.rate),
                obj.zhalaqy,
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=zhukteme_export.xlsx'
        wb.save(response)
        return response

    export_as_excel.short_description = "Exel арқылы сақтау"

    def go_to_public_page(self, request, queryset):
        return HttpResponseRedirect('/zhukteme/')  #

    go_to_public_page.short_description="Толық көру"



