from pathlib import Path
from html import escape

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
INK='#243d32'; GREEN='#d9e9d4'; ORANGE='#f4c7a2'; BLUE='#d9e7ef'; PAPER='#f9f9f3'; MUTED='#5b6b60'

def rect(x,y,w,h,fill=GREEN,r=12,stroke='none'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
def text(x,y,s,size=18,color=INK,weight=400):
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(s)}</text>'
def line(x,y,x2,y2,color=INK,arrow=False):
    return f'<path d="M{x} {y} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="2"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def save(name,title,desc,body,w=800,h=460):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="{INK}" stroke-width="1.5"/></marker></defs>
{rect(0,0,w,h,PAPER,20)}{text(32,45,title,23,weight=600)}{body}</svg>'''
    (ASSETS/f'{name}.svg').write_text(svg)

def create():
    ASSETS.mkdir(exist_ok=True)
    b=rect(32,80,736,340,'#eef1e7')+text(55,114,'html',20,weight=600)
    b+=rect(60,140,300,245,BLUE)+text(82,175,'head · page information',19,weight=600)
    for i,s in enumerate(['Character encoding','Viewport settings','Browser-tab title']): b+=text(85,225+i*48,s)
    b+=rect(390,140,348,245,GREEN)+text(414,175,'body · visible content',19,weight=600)
    b+=text(414,231,'Your next adventure',26,weight=600)+text(414,275,'A heading introduces the page.',17)+text(414,315,'A paragraph explains it.',17)+text(414,355,'A link takes you somewhere.',17)
    save('document','A page has two different jobs','The html element contains head with document information and body with visible content.',b)

    b=''
    for i,(label,note) in enumerate([('block','A new line; auto width usually fills it.'),('inline','Part of a text line; width does not size a span.'),('inline-block','An inline box that accepts width and height.')]):
        y=85+i*114;b+=text(32,y,label,20,weight=600)+text(210,y,note,16)
        b+=rect(210,y+16,554,66,'#eaf0e5',6)
        if i==0: b+=rect(222,y+23,530,23,GREEN,4)+rect(222,y+52,530,23,ORANGE,4)+text(234,y+40,'A',14)+text(234,y+69,'B',14)
        else:
            width=68 if i==1 else 160
            b+=rect(222,y+28,width,37,GREEN,4)+text(236,y+52,'A')+rect(234+width,y+28,width,37,ORANGE,4)+text(248+width,y+52,'B')
    save('display','Same content. Different flow.','Block items occupy separate lines. Inline items fit their text. Inline-block items share a line but accept a width.',b)

    b=rect(95,80,610,335,ORANGE,10)+text(115,108,'MARGIN · outside space',16,weight=600)
    b+=rect(140,125,520,245,INK,4)+text(158,152,'BORDER · the edge',16,'#ffffff',600)
    b+=rect(150,165,500,195,GREEN,0)+text(170,193,'PADDING · breathing room',16,weight=600)
    b+=rect(217,215,366,95,BLUE,4)+text(303,270,'CONTENT',24,weight=600)
    b+=text(180,445,'border-box width = content + padding + border',18)
    save('box-model','Meet the four layers of a box','From outside to inside: orange margin, dark border, green padding, blue content. Border-box includes content, padding and border but not margin.',b)

    b=''
    steps=[('01','Does the rule apply?','Selector and conditions match.'),('02','Which priority group?','Origin, importance, and layers.'),('03','Which selector is more specific?','IDs → classes / attributes → types.'),('04','How close is its scope?','Relevant when scoped rules otherwise tie.'),('05','Which comes last?','Source order breaks the remaining tie.')]
    for i,(n,title,sub) in enumerate(steps):
        y=78+i*72;b+=rect(32,y,736,60,GREEN if i%2==0 else '#eef1e7',8)+text(48,y+36,n,18,MUTED)+text(95,y+25,title,18,weight=600)+text(95,y+47,sub,14,MUTED)
    save('cascade','Specificity is one step, not the whole story','Five cascade decisions: relevance; origin importance and layers; specificity; scoping proximity; source order.',b)

    b=''
    for i,(name,desc) in enumerate([('static','Normal flow; offsets do not reposition it.'),('relative','Keeps its space; its visual box can move.'),('absolute','Out of flow; placed inside its containing block.'),('fixed','Out of flow; often pinned to the viewport.'),('sticky','In flow; sticks within scroll and container limits.')]):
        y=80+i*70;b+=rect(32,y,736,59,'#eef1e7',6)+text(49,y+24,name,18,weight=600)+text(49,y+45,desc,14,MUTED)
        for j in range(3):b+=rect(596+j*48,y+18,35,24,GREEN if j!=1 else ORANGE,3)
        if i in [1,2]:b+=rect(650,y+6,35,24,INK,3)
    save('position','Five ways to place a box','Comparison of static, relative, absolute, fixed and sticky positioning. Fixed containing blocks can be changed by certain ancestors.',b)

    b=text(34,82,'flex-direction: row · horizontal writing mode',17,MUTED)
    b+=rect(70,130,660,210,'#eaf0e5',9)
    for i,w in enumerate([125,160,125]):
        x=[100,280,495][i];b+=rect(x,185,w,100,[GREEN,ORANGE,BLUE][i],8)+text(x+20,244,f'Item {i+1}',20,weight=600)
    b+=line(75,110,725,110,arrow=True)+text(245,101,'MAIN AXIS · justify-content',16,weight=600)
    b+=line(48,135,48,340,arrow=True)+text(77,376,'CROSS AXIS · align-items (vertical here)',17,weight=600)
    b+=text(77,417,'Switch to column and the axes switch roles.',17,MUTED)
    save('flex','Flexbox follows axes, not screen directions','For a horizontal row, the main axis runs left to right and the cross axis runs top to bottom. justify-content uses the main axis; align-items uses the cross axis.',b)

    b=text(34,85,'Rows + columns + intentional gaps',18,MUTED)
    for col in range(3): b+=text(160+col*205,118,f'Column {col+1}',16,MUTED)
    for row in range(2):
        b+=text(32,202+row*125,f'Row {row+1}',15,MUTED)
        for col in range(3):
            x=135+col*205;y=140+row*125;b+=rect(x,y,180,105,[GREEN,ORANGE,BLUE][col],8)+text(x+48,y+60,f'{row+1} / {col+1}',20,weight=600)
    b+=text(135,414,'A track is a row or column. A cell is one intersection.',17)
    save('grid','A layout you can sketch first','A two-row three-column grid, with each cell labelled by row and column. Gaps separate tracks.',b)

    b=rect(32,99,465,290,'#e9eee3',12)+rect(48,116,433,28,INK,6)
    b+=rect(48,163,116,207,GREEN,7)+text(65,193,'Sidebar',16)
    for row in range(2):
        for col in range(2): b+=rect(184+col*151,163+row*110,135,97,ORANGE if col==0 else BLUE,7)
    b+=rect(559,72,194,357,INK,20)+rect(570,88,172,324,'#eef2e8',12)+rect(582,108,148,29,GREEN,5)
    for i in range(3):b+=rect(582,150+i*83,148,69,[ORANGE,BLUE,GREEN][i],5)
    b+=text(50,424,'Room to sit side by side',17)+text(568,451,'Room to stack',17)
    save('responsive','The content stays. The arrangement adapts.','A wide dashboard has a sidebar and two card columns. A narrow phone layout stacks the same content in one column.',b)

    b=rect(32,93,735,309,'#edf1e7',10)+text(52,125,'ONE VIEWPORT · two different container widths',17,weight=600)
    b+=rect(53,151,220,230,'#ffffff',8)+rect(70,168,185,84,GREEN,5)+text(71,285,'Narrow slot',20,weight=600)+text(71,318,'Stack the content.',16)
    b+=rect(295,151,450,230,'#ffffff',8)+rect(315,174,160,180,GREEN,5)+text(498,230,'Wide slot',20,weight=600)+text(498,265,'Place content',16)+text(498,289,'side by side.',16)
    b+=text(45,439,'@container responds to an ancestor; @media responds to the viewport.',17)
    save('container','Same card. Different spaces.','Two containers within one viewport. A narrow card stacks image and text; a wide card puts them beside each other.',b)

    b=rect(25,75,750,355,'#edf2e5',16)+text(55,115,'STRUCTURE → STYLE → LAYOUT',14,MUTED,600)
    b+=rect(73,159,326,224,'#ffffff',14, '#c7d5c3')+rect(73,159,326,36,INK,14)
    b+=text(91,183,'your-first-page.html',13,'#ffffff')+text(96,240,'Hello, web.',32,weight=600)+rect(97,262,204,8,GREEN,4)+rect(97,281,257,8,GREEN,4)+rect(97,317,114,35,ORANGE,6)+text(112,340,'Explore →',16)
    b+=rect(425,127,307,199,GREEN,14, '#bdcfb8')+text(449,164,'.a-little-curiosity {',17,weight=600)+text(465,206,'display: grid;',18)+text(465,242,'gap: 1rem;',18)+text(449,283,'}',18)
    b+=rect(502,346,182,55,ORANGE,28)+text(523,381,'Made to make sense.',14,weight=600)
    save('hero','Small ideas. Real things you can build.','A diagram of an HTML browser page alongside a CSS rule card, illustrating structure, style and layout.',b)

    b=rect(0,0,800,480,'#e5eedb',0)+ '<circle cx="640" cy="110" r="65" fill="#f4c7a2"/>'
    b+='<path d="M0 380Q200 300 400 370T800 330V480H0Z" fill="#cedfbc"/>'
    for cx in [242,570]: b+=f'<circle cx="{cx}" cy="322" r="102" fill="#f9f9f3" stroke="#253e32" stroke-width="12"/><circle cx="{cx}" cy="322" r="6" fill="#253e32"/>'
    b+='<path d="M242 322L329 185L417 322Z M329 185L522 185L417 322 M522 185L570 322 M522 185L510 139L551 129 M329 185L317 146" fill="none" stroke="#3b7859" stroke-width="14" stroke-linejoin="round"/>'
    b+='<path d="M292 146H340 M399 322H442 M442 322L454 346" stroke="#253e32" stroke-width="12" stroke-linecap="round" fill="none"/>'
    save('bicycle','', 'An original green city bicycle illustration beside a warm sun.',b,800,480)

if __name__=='__main__': create()
