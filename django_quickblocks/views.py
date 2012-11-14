from .models import *
from smartmin.views import *
from django import forms

class QuickBlockCRUDL(SmartCRUDL):
    model = QuickBlock
    permissions = True
    actions = ('create', 'update', 'list')

    class Update(SmartUpdateView):
        fields = ('title', 'summary', 'content', 'image', 'link', 'video_id', 'quickblock_type', 'is_active')

        def pre_save(self, obj):
            obj = super(QuickBlockCRUDL.Update, self).pre_save(obj)
            obj.space_tags()
            return obj

        def derive_exclude(self):
            exclude = super(QuickBlockCRUDL.Update, self).derive_exclude()

            block_type = self.object.quickblock_type

            if not block_type.has_summary:
                exclude.append('summary')

            if not block_type.has_video:
                exclude.append('video_id')

            if not block_type.has_title:
                exclude.append('title')

            if not block_type.has_tags:
                exclude.append('tags')

            if not block_type.has_image:
                exclude.append('image')

            if not block_type.has_link:
                exclude.append('link')

            return exclude

        def get_context_data(self, *args, **kwargs):
            context = super(QuickBlockCRUDL.Update, self).get_context_data(*args, **kwargs)
            context['type'] = self.object.quickblock_type
            return context

        def derive_title(self):
            return "Edit %s" % self.object.quickblock_type.name

    class Create(SmartCreateView):
        grant_permissions = ('django_quickblocks.change_quickblock',)

        def derive_exclude(self):
            exclude = super(QuickBlockCRUDL.Create, self).derive_exclude()

            block_type = self.get_type()
            if block_type:
                exclude.append('quickblock_type')

                if not block_type.has_summary:
                    exclude.append('summary')

                if not block_type.has_video:
                    exclude.append('video_id')

                if not block_type.has_title:
                    exclude.append('title')

                if not block_type.has_tags:
                    exclude.append('tags')

                if not block_type.has_image:
                    exclude.append('image')

                if not block_type.has_link:
                    exclude.append('link')

            return exclude

        def derive_title(self):
            block_type = self.get_type()
            if block_type:
                return "Create %s" % block_type.name
            else:
                return "Create Quickblock"

        def get_type(self):
            if 'type' in self.request.REQUEST:
                return QuickBlockType.objects.get(id=self.request.REQUEST.get('type'))
            return None

        def get_context_data(self, *args, **kwargs):
            context = super(QuickBlockCRUDL.Create, self).get_context_data(*args, **kwargs)
            context['type'] = self.get_type()
            return context

        def pre_save(self, obj):
            obj = super(QuickBlockCRUDL.Create, self).pre_save(obj)

            block_type = self.get_type()
            if block_type:
                obj.quickblock_type = block_type
            
            obj.space_tags()
            return obj
            
    class List(SmartListView):
        fields = ('title', 'priority', 'quickblock_type', 'tags')
        link_fields = ('title',)
        default_order = '-modified_on'
        search_fields = ('title__icontains', 'content__icontains', 'summary__icontains')

        def get_context_data(self, *args, **kwargs):
            context = super(QuickBlockCRUDL.List, self).get_context_data(*args, **kwargs)
            context['types'] = QuickBlockType.objects.all()
            return context

class QuickBlockTypeCRUDL(SmartCRUDL):
    model = QuickBlockType
    permissions = True
    actions = ('create', 'update', 'list')

    class List(SmartListView):
        fields = ('name', 'slug', 'description')
        link_fields = ('name',)

