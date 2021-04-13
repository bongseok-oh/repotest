from django import forms

# 파일을 업로드 하기 위한 Form Type 정의
class FileListForm(forms.Form):
    tester = forms.CharField(max_length=255)
    origin_file = forms.FileField(label='PPTX or HTML File')
    desc = forms.CharField(max_length=255)