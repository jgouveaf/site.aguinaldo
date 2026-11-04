"""QA de navegador. Use com servidor local; cria uma partida QA identificada no banco."""
from playwright.sync_api import sync_playwright, expect
from pathlib import Path
import ast, json, os
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evidencias';OUT.mkdir(exist_ok=True)
URL=os.environ.get('QA_SITE_URL','http://127.0.0.1:8765')
answers={}
for line in (ROOT/'sql/setup.sql').read_text(encoding='utf-8').splitlines():
 if line.startswith("('"):
  row=ast.literal_eval(line.rstrip(',').rstrip(';'));answers[row[0]]=row[-2]
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL,wait_until='networkidle')
 expect(page.locator('.mode-choice')).to_have_count(3)
 expect(page.locator('#ranking')).to_be_visible()
 page.locator('#ranking-section').screenshot(path=str(OUT/'ranking-python.png'))
 page.locator('#nickname').fill('QA Web 04-11')
 page.locator('#start-button').click()
 seen=[];levels=[];captured=[]
 def intercept(route):
  data=route.request.post_data_json
  if data.get('action')=='answer' and data.get('index')==8:
   captured.append(data)
   if len(captured)==1:
    # O servidor recebe e salva, mas o navegador perde a resposta.
    route.fetch()
    route.abort('failed')
    return
  route.continue_()
 page.route('**/functions/v1/web-game',intercept)
 for i in range(9):
  expect(page.locator('#question-count')).to_have_text(f'Questão {i+1} de 9')
  expect(page.locator('#options button').first).to_be_enabled()
  question=page.locator('#question-text').inner_text()
  assert question not in seen,question
  seen.append(question);levels.append(page.locator('#question-level').inner_text())
  if i==0:page.locator('.play-layout').screenshot(path=str(OUT/'partida-navegador.png'))
  page.locator(f'[data-answer="{answers[question]}"]').click()
 expect(page.locator('#retry-answer')).to_be_visible()
 expect(page.locator('#options button').first).to_be_disabled()
 page.locator('#retry-answer').click()
 expect(page.locator('#result-stage')).to_be_visible()
 assert captured[0]==captured[1],captured
 assert levels==['Fácil']*3+['Média']*3+['Difícil']*3,levels
 expect(page.locator('#result-prize')).to_contain_text('1.000.000,00')
 expect(page.locator('#ranking tbody')).to_contain_text('QA Web 04-11')
 page.locator('.play-layout').screenshot(path=str(OUT/'resultado-navegador.png'))
 # Falhas de leitura são simuladas no transporte; não alteram o banco.
 page.route('**/rest/v1/rpc/ranking_public',lambda r:r.fulfill(status=200,content_type='application/json',body='[]'))
 page.locator('#refresh').click()
 expect(page.locator('#status')).to_have_text('Ainda não há resultados para este jogo.')
 page.unroute('**/rest/v1/rpc/ranking_public')
 page.route('**/rest/v1/rpc/ranking_public',lambda r:r.fulfill(status=503,content_type='application/json',body='{}'))
 page.locator('#refresh').click()
 expect(page.locator('#status')).to_contain_text('Falha ao consultar ranking')
 expect(page.locator('#connection-status')).to_have_text('Conexão indisponível')
 page.unroute('**/rest/v1/rpc/ranking_public')
 page.locator('#refresh').click()
 expect(page.locator('#ranking')).to_be_visible()
 widths=[]
 for width in [320,375,390,768,1440]:
  page.set_viewport_size({'width':width,'height':900})
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  widths.append(width)
 page.emulate_media(reduced_motion='reduce')
 assert page.evaluate("getComputedStyle(document.documentElement).scrollBehavior")=='auto'
 page.reload(wait_until='networkidle')
 expect(page.locator('#ranking tbody')).to_contain_text('QA Python 04-11')
 page.evaluate('window.scrollTo(0,0); document.activeElement.blur()')
 page.screenshot(path=str(OUT/'site-desktop.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844})
 page.screenshot(path=str(OUT/'site-celular.png'),full_page=True)
 assert not errors,errors
 result={'site':URL,'nine_correct':True,'unique_questions':len(seen),'levels':levels,'lost_final_response_retry':True,'identical_resend_payload':captured[0]==captured[1],'empty_and_error_ui':True,'persisted_after_reload':True,'viewport_widths_without_overflow':widths,'reduced_motion':True,'javascript_errors':errors,'session_id':captured[0]['session_id']}
 (OUT/'browser-tests.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False))
 browser.close()
