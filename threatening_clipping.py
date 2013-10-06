# -*- coding: utf-8 -*-

"""
脅迫状の一つ一つの文字
（新聞記事の切り抜き）
"""

from probability import get_by_probability

from setting import mplus, bokutachi, kirieji, tanuki, seto


class Clipping(object):
	# 一つ一つの文字のサイズ
	CLIPPING_WIDTH = 300
	CLIPPING_HEIGHT = 400

	""" 新聞記事の切り抜きのクラス """
	def __init__(self, character):
		self._calculate_clippingsize()
		self.background = Background()
		self.character_style = CharacterStyle(character, self.background.backcolor)
		self.press = Press()

	""" 切り抜きの実際のサイズを計算する """
	def _calculate_clippingsize(self):
		# 新聞の基準サイズとの差を求める
		gap_min = 0
		gap_max = 61
		step = 15
		gap_probability = dict([(i, 10) for i in xrange(gap_min, gap_max, step)])
		width_gap = get_by_probability(gap_probability)
		height_gap = get_by_probability(gap_probability)
		# 実際のサイズ
		self.width = Clipping.CLIPPING_WIDTH - width_gap
		self.height = Clipping.CLIPPING_HEIGHT - height_gap

	def __str__(self):
		return "<Clipping w:{0} h:{1} back:{2} character:{3} press:{4}>".format(self.width, self.height, self.background, self.character_style, self.press)


class Background(object):
	""" 新聞記事の背景のクラス """
	def __init__(self):
		# 背景色
		backcolor_probability = {(105, 105, 105): 10, (137, 137, 137): 10, (169, 169, 169): 10, (201, 201, 201): 10}
		self.backcolor = get_by_probability(backcolor_probability)
		
		# 背景が単色かストライプか
		is_solid = get_by_probability({True: 100, False: 50})

		# 背景が単色なら何もしない，ストライプ柄なら設定
		if is_solid:
			self.stripelinecolor = None
			self.stripelinewidth = None
		else:
			linecolor_probability = {(87,87,87): 10, (128,128,128): 10, (169,169,169): 10, (210, 210, 210): 10}
			linewidth_probability = {2: 10, 5: 10, 8: 10}
			self.stripelinecolor = get_by_probability(linecolor_probability)
			self.stripelinewidth = get_by_probability(linewidth_probability)

	def __str__(self):
		return "<Background color:{0} linecolor:{1} linewidth:{2}>".format(self.backcolor, self.stripelinecolor, self.stripelinewidth)


class CharacterStyle(object):
	""" 文字スタイルのクラス """
	def __init__(self, character, backgroundcolor):
		self.character = character

		# 文字サイズを決める
		textsize_probability = {150: 10, 200: 10, 250: 10, 300: 10}
		self.size = get_by_probability(textsize_probability)

		# フォントを決める
		font_probability = {mplus: 10, bokutachi: 10, kirieji: 10, tanuki: 10, seto: 10}
		self.font = get_by_probability(font_probability)

		# 文字色を決める
		# 濃い背景の場合だけ白っぽい文字色を許す
		# 普通は黒色
		if backgroundcolor[0] < 150:
			textcolor_probability = {(0, 0, 0): 10, (255, 255, 255): 10, (239, 239, 239): 10}
			self.color = get_by_probability(textcolor_probability)
		else:
			self.color = (0, 0, 0)

	def __str__(self):
		return "<CharacterStyle chara:{0} size:{1} font:{2} color:{3}>".format(self.character.encode("utf-8"), self.size, self.font, self.color)


class Press(object):
	# 圧縮する方向
	# 垂直方向
	VER = 0
	# 水平方向
	HOR = 1

	""" 切り抜きの圧縮のクラス """
	def __init__(self):
		# 圧縮方向を決める
		direction_probability = {Press.VER: 10, Press.HOR: 10}
		self.direction = get_by_probability(direction_probability)

		# 圧縮率を決める
		ratio_probability = {0.6: 10, 0.7: 10, 0.8: 10}
		self.ratio = get_by_probability(ratio_probability)

	def __str__(self):
		return "<Press dir:{0} ratio:{1}>".format(self.direction, self.ratio)
		





