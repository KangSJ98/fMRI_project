def initiate():
    def basicConfig():
        """
        subject 정보
        eyelink 시작
        """
    def makeScreenComponents():
        """
        스크린 변수
        모양 크기
        카드 좌표 정보
        옵션 좌표 정보
        """
    
def calculateAnswerCard(card1, card2, opt):
    """
    card1, card2 입력받아서 정답 카드 반환
    return : answercard
    """

def card():
    """
    card 객체 생성
    기본 원,검정,filled,1
    isequal(obj1,obj2) -> 4개가 다 같아야 true
    """

def drawBackground(opt):
    """
    스크린 전체 회색 배경, card1,2,3 테두리, option들 테두리 그리기
    """

def drawCard(card, center_x, center_Y, opt):
    """
    해당 x,y좌표에 카드 정보에 해당하는 도형 그리기
    """

def eyelinkPrep(opt):
    """
    eyelink 초기 세팅
    enter, c, v
    """

def selectRandomCard(opt):
    """
    return : 무작위 카드 반환
    """

def trialReset(opt):
    """
    opt.card1, opt.card2 선택
    opt.answerCard 계산
    opt.playerCard 초기화
    """

def updateScreen(opt, data):
    """
    part 1 : 그림그리기
    background 그림
    card 1,2 그림
    


    pard 2 : 데이터 저장
    data 저장
    """


def makeCard(opt, data):


"""
만약 선택을 한다면 옵션 선택한 화면을 보여주는 phase로 넘어감. 이때는 입력을 받지 않음
if opt.chooseOption = 1
"""