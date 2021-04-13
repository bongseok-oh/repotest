
def index(request): 
    # 메인 리스트 뷰  (FBV)
    currentUser = request.session.get('adid', False)        #bongseok.oh 권한 통제를 위한 사용자 정보 가져오기 
    template_name = "manual/check.html"
    if request.method == "POST": # 파일 업로드 요청 시
        # print(request.FILES)
        try:
            newPost = CompareWord(
                tester = request.POST['tester'],
                desc = request.POST['desc'],
                origin_file = request.FILES['test_file'],
                comp = request.POST['comp'],
            )
            newPost.save() # 파일 및 정보를 저장
        except:
            return redirect(reverse_lazy('list')) # 메인 리스트로 이동(리프레시)
        return redirect(reverse_lazy('list')) # 메인 리스트로 이동(리프레시)
    else: # 페이지 로드 시
        forms = FileListForm()
        object_list = CompareWord.objects.order_by('-id') # 히스토리를 DB에서 가져옴
        return render(request, template_name, {'forms':forms, 'object_list':object_list, 'user':currentUser}) #bongseok.oh 권한 통제를 위해 currnetUser 받음

def word_list(request): # 단어 리스트 뷰 (FBV)
    currentUser = request.session.get('adid', False)
    template_name = "manual/word_list.html"
    if request.GET:
        try:

            word = request.GET['word'] # 검색 단어 
        except:
            word = ''
    else:
        word = ''
    models = WordDict.objects.all().filter(Q(word__icontains=word)).order_by('-id')  # DB에서 검색하여 저장
    context = {'object_list':models, 'word':word, 'user':currentUser}
    return render(request, template_name, context)

class WordDictCreateView(CreateView): # 단어 생성 뷰 (CBV)
    model = WordDict
    template_name = "manual/word_modify.html"
    fields = ['word','word_type', 'desc']
    success_url = reverse_lazy('word_list')

class WordDictUpdateView(UpdateView): # 단어 업데이트 뷰 (CBV)
    model = WordDict
    template_name = "manual/word_modify.html"
    fields = ['word', 'word_type', 'desc']
    success_url = reverse_lazy('word_list')

class WordDictDeleteView(DeleteView): # 단어 삭제 뷰 (CBV)
    model = WordDict
    template_name = "manual/word_confirm_delete.html"
    success_url = reverse_lazy('word_list')


def compare(request, pk): # 단어 Compare 로직
    querySet = CompareWord.objects.get(pk=pk) 
    # ref_words = [word['word'] for word in WordDict.objects.all().values('word')] # 단어 사전 리스트 Get
    ref_word = WordDict.objects.all().exclude(word_type='JTBC').values_list('word', flat=True) # 단어 사전 리스트 Get
    korean_words = WordDict.objects.all().filter(word_type='BASE').values_list('word', flat=True) # 국립국어원 단어 Get
    he_words = WordDict.objects.all().filter(word_type='HE').values_list('word', flat=True) # HE본부용 단어 Get
    ha_words = WordDict.objects.all().filter(word_type='HA').values_list('word', flat=True) # HA본부용 단어 Get
    mc_words = WordDict.objects.all().filter(word_type='MC').values_list('word', flat=True) # MC본부용 단어 Get
    lg_names = WordDict.objects.all().filter(word_type='LGE_name').values_list('word', flat=True) # LG전자 기능 고유명사 Get
    jtbc_words = WordDict.objects.all().filter(word_type='JTBC').values_list('word', flat=True) # JTBC 이슈 단어 Get
    origin_file = querySet.origin_file # 업로드된 파일 
    result_file = 'Result_'+origin_file.name.split('/')[-1] # 저장된 파일 이름
    result_file_path = '/'.join(origin_file.name.split('/')[:-1]) # 표시 될 파일의 경로
    pptx_path = '\\'.join(origin_file.path.split('\\')[:-1]) + '\\' + result_file # DB 에 적재될 절대 경로
    paragraph_list = [] # PPT의 문단을 담기 위한 빈 List

    common_words = korean_words | lg_names | he_words | ha_words | mc_words        # 공통 선택했을 때 기본 단어셋 (국립국어원 + HE + HA + MC)
    common_he = korean_words | lg_names | he_words                                 # HE 선택 했을 때 기본 단어셋 (국립국어원 + HE)
    common_ha = korean_words | lg_names | ha_words                                 # HA 선택 했을 때 기본 단어셋 (국립국어원 + HA)
    common_mc = korean_words | lg_names | mc_words                                 # MC 선택 했을 때 기본 단어셋 (국립국어원 + MC)

    #company = CompareWord.objects.values_list('comp', flat=True)         # 얘를 어떻게 가져와야 하는지???
    company = [comp['comp'] for comp in CompareWord.objects.all().values('comp').order_by('-date')]
    company = company[0]

    if str(company) == 'common':
        ref_words = common_words
    elif str(company) == 'he':
        ref_words = common_he
    elif str(company) == 'ha':
        ref_words = common_ha
    elif str(company) == 'mc':
        ref_words = common_mc
    else:
        ref_words = ref_word          # 실제로 적용시에는 84열 ref_word로 변경하여 사용 예정

#################################
########### pptx case ###########
#################################

    if str(origin_file).split('.')[-1] == 'pptx':
        try:
            ptx = Presentation(origin_file) # PPT 파일 로드
        except Exception as e:
            print(e)
            return redirect(reverse_lazy('list'))


#################################
########### html case ###########
#################################

    elif str(origin_file).split('.')[-1] == 'html' or str(origin_file).split('.')[-1] == 'htm':
        decoded_html = origin_file.read().decode('utf-8')
        soup = bs(decoded_html, 'html.parser')

##################################
############ pdf case ############
##################################

    elif str(origin_file).split('.')[-1] == 'pdf':

        with open(origin_file.path, 'rb') as f:
            pdf = pdftotext.PDF(f)

        paragraph = '\n'.join(pdf)
        
        if len(paragraph) == 0: # 판정 결과 
            results = '<span style="font-size:1.0em; color:green;"><b>PASS</b></span>'
        else:
            results = '<span style="font-size:1.0em; color:red;"><b>NG</b></span></br>'
            results += '<span style="font-size:1.0em;"><b>Bad Words : {} (Total Words: {} / Bad Words Sum: {})</b></span></br></br>'.format(len(paragraph), len(paragraph),paragraph)

      #JTBC 단어는 색상 구분
               
        result = str(company)                                                          #JTBC 단어 구분하여 결과 표시
        querySet.result = result
        querySet.save() # DB 저장

        return redirect(reverse_lazy('list'))

def comparehtml(request, pk):

    return 'ok'


