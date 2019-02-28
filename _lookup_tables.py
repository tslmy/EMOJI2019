# Prepare lookup tables
import pandas as pd

try:
    wiki_df = pd.read_csv('Wikipedia_list_of_emojis.csv')
except:
    wiki_df = pd.read_html('https://commons.wikimedia.org/wiki/Data:Emoji.tab')[0]
    wiki_df.columns = ['emj', 'unicode', 'name', 'kw']
    wiki_df.to_csv('Wikipedia_list_of_emojis.csv', index=False)
emj2unicode = wiki_df.set_index('emj').unicode
unicode2emj = wiki_df.set_index('unicode').emj

try:
    emj_ucCtgy = pd.read_csv('Unicode_list_of_emojis.csv').set_index('emoji').category
except:
    html_df = pd.read_html('https://unicode.org/emoji/charts/full-emoji-list.html')[0]
    df = html_df[[0, 1, 2, 14]]
    df.columns = ['name', 'unicode', 'emoji', 'description']
    index_titles = df.isna().any(axis=1)
    titles_df = df[index_titles]
    titles = titles_df[titles_df.name.str.istitle()].name
    wCate_df = df.assign(category=titles.reindex(df.index).fillna(method='ffill')).dropna(how='any')
    wCate_df = wCate_df[wCate_df.name!='№'].drop('name', axis=1)
    wCate_df.to_csv('Unicode_list_of_emojis.csv', index=False)
    emj_ucCtgy = wCate_df.set_index('emoji').category
ucCtgys = ['Smileys & Emotion', 'People & Body', 'Animals & Nature', 'Food & Drink', 'Travel & Places', 'Activities', 'Objects', 'Symbols']

from glob import glob
emj_img_fpaths = pd.Series(glob('apple_emoji_images/*.png'), name='emj_img_fpath')
emj_img_codes = emj_img_fpaths.str[len('apple_emoji_images/'):].apply(lambda fpath: fpath[fpath.find('_')+1:-4]).rename('emj_img_code')
emj_img_codes.index = emj_img_fpaths
_ = emj_img_codes.str.startswith('emoji-modifier-fitzpatrick-type-')
emj_img_codes.loc[_] = emj_img_codes.loc[_].str[len('emoji-modifier-fitzpatrick-type-')+2:-6]
_ = emj_img_codes.str.startswith('2_')
emj_img_codes.loc[_] = emj_img_codes.loc[_].str[2:]
unicode2imgpath = emj_img_codes.reset_index().set_index('emj_img_code').emj_img_fpath
from matplotlib import pyplot as plt
unicode2img = unicode2imgpath.apply(plt.imread)

# Constants:
emjs_common = ['📙', '🍥', '🔄', '🏇', '🍈', '🐨', '👐', '🔳', '🐞', '📀', '🐜', '👾', '🔆', '🙎', '🐺', '🔅', '🐂', '☸', '🐓', '🌕', '📦', '🐇', '☠', '🍐', '🎽', '🐘', '☯', '🌾', '🔻', '🚧', '👒', '🍄', '🐔', '👹', '🔝', '🍏', '😾', '🚓', '🐢', '🐑', '🐉', '🔵', '🆓', '🐛', '🐡', '📕', '🚑', '🈂', '🚢', '🔞', '🐆', '🈹', '🎑', '👄', '👥', '🃏', '🐄', '🚹', '🎻', '🌲', '🔯', '💶', '👷', '☃', '🔰', '☹', '☢', '📌', '🗽', '🕛', '📘', '🐯', '🎋', '💊', '👲', '✍', '🎠', '🎅', '🅾', '🍘', '🎯', '🌰', '🔸', '🐎', '🌽', '💒', '♥', '🎨', '🎮', '🐖', '🔹', '🐚', '⏩', '🏩', '🎄', '🐮', '🕔', '➰', '🍡', '🐴', '🌂', '📲', '✔', '🐧', '🌜', '✝', '🗾', '🏢', '🎫', '🐦', '🔜', '🐍', '🕓', '☂', '✅', '🏁', '🐵', '🚋', '❕', '🍂', '🐽', '💴', '🔴', '💳', '🌎', '🐹', '🌌', '🍢', '🕒', '💿', '🌐', '🚄', '🉐', '🈲', '🍎', '📣', '👓', '🛀', '🔔', '😯', '😀', '🎇', '🚫', '🚣', '🐒', '🌁', '🎷', '🍙', '🏊', '🐙', '🐳', '🎈', '🐋', '🎐', '🚅', '🎌', '👘', '🍋', '👱', '✡', '🗼', '🕧', '👳', '🍶', '🚪', '💯', '🐕', '🏨', '👚', '🚀', '🍇', '😸', '❎', '🏆', '🍅', '🐅', '🏂', '🌍', '🎍', '🍼', '🆕', '😛', '🌋', '🌱', '💠', '👖', '⏰', '⚛', '🐸', '🎃', '🎺', '🚘', '👽', '😹', '🚇', '🐝', '🐈', '☮', '😺', '🙉', '🌏', '🏥', '➕', '👜', '🍍', '🏤', '🍑', '🐗', '🚺', '❔', '🐥', '📚', '🔧', '🚃', '👵', '😗', '🍯', '👮', '💮', '👞', '👿', '🎩', '💇', '🎴', '💺', '🐁', '😼', '🎧', '♀', '🌳', '👬', '🚬', '👃', '🍱', '🍣', '🚥', '👰', '🍸', '👕', '🚚', '🌚', '🚭', '🚿', '🌄', '🏪', '🍊', '🎡', '🍳', '📱', '🌊', '🆚', '👛', '👆', '🐤', '😽', '🔛', '🚐', '👝', '👇', '👣', '🐾', '🚸', '🔱', '🕥', '🌿', '🔪', '💣', '🚁', '🐭', '🍆', '🏰', '🏄', '🔙', '😧', '🎬', '🐬', '🕢', '💻', '📍', '👪', '🔑', '🎲', '📞', '📯', '🍹', '👨', '©', '🚏', '😶', '🏫', '🚕', '😦', '🐠', '🔶', '🌅', '🚙', '🌝', '💀', '📗', '👦', '🍟', '🎳', '🚲', '🚉', '👂', '🎹', '🍵', '🍔', '🎓', '🆗', '📝', '💉', '🍩', '🍨', '💬', '🎪', '🛁', '🏦', '🆘', '😟', '👩', '😙', '😿', '🕖', '🔊', '🍬', '👻', '🔍', '🐣', '🚼', '♂', '❌', '🕕', '➿', '🆙', '😬', '🌃', '🚌', '🍕', '🌷', '💐', '🚨', '🙍', '🚶', '👴', '🍞', '🔃', '🍗', '🍮', '⚜', '🅰', '🌠', '®', '🎢', '🍌', '🍧', '😈', '🎣', '💾', '🔺', '😐', '🌛', '👔', '🍷', '💆', '👧', '🌇', '🎾', '🍚', '💡', '📢', '🎆', '🚂', '🐟', '🎒', '😮', '🚦', '😕', '🆔', '🆖', '🍁', '™', '👶', '🐼', '🎿', '🍲', '🙀', '🚻', '👡', '👢', '🚜', '👟', '🏡', '🔫', '📺', '🎊', '🕑', '🎎', '🚆', '😜', '🍖', '🆒', '👙', '🍃', '🚍', '🎼', '🔚', '🏮', '🔩', '🚤', '💃', '👏', '📰', '🔘', '🎰', '💢', '🔽', '📩', '🈵', '🏭', '💥', '🍛', '👠', '📻', '💈', '💌', '🔁', '🎥', '💩', '🍭', '🕝', '😒', '📎', '🎦', '🕘', '🔌', '🏯', '🌟', '💤', '🍝', '💑', '🙊', '⏪', '🕙', '🏧', '🍪', '🐻', '😃', '😻', '🚝', '🕡', '🍜', '🍫', '📖', '😝', '🔋', '🔭', '🔮', '🏬', '💰', '👈', '🏠', '💧', '🍉', '🌼', '🚈', '🗻', '💸', '🕠', '⏳', '🎸', '🕞', '💟', '🔒', '🚊', '😇', '🚖', '💄', '🍒', '😲', '👉', '🌙', '🈁', '🌈', '🐰', '📓', '📼', '😖', '🏀', '🎁', '🐲', '📵', '🚗', '🚒', '📂', '📡', '🎀', '💁', '🔥', '🚞', '📈', '😠', '👅', '🆑', '🍀', '💼', '🔈', '💏', '🍦', '🐷', '😆', '👸', '🎱', '🔉', '🌹', '🙋', '👌', '🍺', '💪', '💍', '🌀', '😡', '💚', '🌉', '😰', '📶', '🚷', '🍻', '👫', '😤', '🙅', '👭', '👎', '🍓', '😄', '📹', '📟', '🙇', '🌺', '🌴', '😨', '🌆', '💅', '💎', '🌞', '😴', '🌻', '👋', '🔎', '😪', '🐱', '💨', '⏬', '🎉', '💙', '☘', '💛', '👗', '😚', '😵', '🏃', '👼', '💽', '😷', '🔦', '💜', '😌', '🔏', '😥', '💭', '⚔', '💫', '🚔', '🎂', '🔓', '💲', '🙆', '📷', '👑', '🚡', '😉', '❓', '🏉', '🐶', '💝', '💘', '🙏', '😏', '😎', '🙈', '😅', '🏣', '😁', '🏈', '💋', '🙌', '💷', '😣', '👍', '😫', '😞', '🍰', '😱', '🎤', '👯', '😍', '😳', '💔', '😓', '😂', '👀', '💖', '🎵', '🌸', '✨', '💞', '💵', '😑', '😘', '✊', '💦', '😭', '💓', '🎶', '😔', '💗', '😊', '👊', '💕', '✋', '😩', '😢', '🍴', '😋']
basic_emotion_tokens = ["😊", "😢", "😱", "😡", "😲"]
emjs_face            = ["😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊", "😋", "😎", "😍", "😘", "😗", "😙", "😚", "☺", "🙂", "🤗", "🤩", "🤔", "🤨", "😐", "😑", "😶", "🙄", "😏", "😣", "😥", "😮", "🤐", "😯", "😪", "😫", "😴", "😌", "😛", "😜", "😝", "🤤", "😒", "😓", "😔", "😕", "🙃", "🤑", "😲", "☹", "🙁", "😖", "😞", "😟", "😤", "😢", "😭", "😦", "😧", "😨", "😩", "🤯", "😬", "😰", "😱", "😳", "🤪", "😵", "😡", "😠", "🤬", "😷", "🤒", "🤕", "🤢", "🤮", "🤧", "😇", "🤠", "🤡", "🤥", "🤫", "🤭", "🧐", "🤓"]

liwc_top_lv_ctgys = ['Funct', 'Social', 'Affect', 'Cogmech', 'Percept', 'Bio', 'Relativ', 'Personal Concerns', 'Swear', 'Assent']
liwc_categories = \
{'Hear': 'Perceptual processes', 
'Ingest': 'Biological processes', 
'Anger': 'Psychological Processes', 
'Anx': 'Psychological Processes', 
'Body': 'Biological processes', 
'Negemo': 'Psychological Processes', 
'Money': 'Personal concerns', 
'Posemo': 'Psychological Processes',
'Cause': 'Cognitive processes', 
'Motion': 'Relativity', 
'Sexual': 'Biological processes', 
'Quant': 'Other Grammar', 
'Leisure': 'Personal concerns', 
'Certain': 'Cognitive processes', 
'Tentat': 'Cognitive processes',
'Home': 'Personal concerns', 
'See': 'Perceptual processes', 
'Sad': 'Psychological Processes', 
'Work': 'Personal concerns', 
'Death': 'Personal concerns', 
'Family': 'Social processes', 
'Number': 'Other Grammar', 
'Time': 'Relativity',
'Feel': 'Perceptual processes', 
'Negate': 'Linguistic Dimensions', 
'Space': 'Relativity', 
'Relig': 'Personal concerns', 
'Friend': 'Social processes', 
'Health': 'Biological processes', 
'Discrep': 'Cognitive processes',
'Insight': 'Cognitive processes'}