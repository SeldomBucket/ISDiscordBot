from deck import Deck


KINDLED_ITEMS = {
	'ARMORED_GOWN.jpg':								3,
	'BATTLE_SCARF.jpg':								2,
	'BLADED_SORTIR.jpg':							3,
	'BLOOD_BOOTS.jpg':								2,
	'BRAWLER’S_JACKET.jpg':							3,
	'BRONZE_SORTIR.jpg':							1,
	'CODOS_FEATHERED_HAT.jpg':						1,
	'DAETHA_SWORD.jpg':								3,
	'DIAMOND_SORTIR.jpg':							4,
	'DRAVAN_HAT.jpg':								2,
	'EBONY_SORTIR.jpg':								3,
	'EYE_GLOVES.jpg':								1,
	'EYESTALK_HAT.jpg':								1,
	'FIGHTING_BOOTS.jpg':							1,
	'FIGHTING_CAPE.jpg':							2,
	'GLASS_SORTIR.jpg':								1,
	'GOLD_SORTIR.jpg':								2,
	'INDERGLASS_DRESS.jpg':							2,
	'IOLETTA_GOWN.jpg':								1,
	'KALEIDOSCOPE_EYEGLASSES.jpg':					2,
	'KLEUM_MAIL_SHIRT.jpg':							2,
	'MAGMA_CLOAK.jpg':								3,
	'MELISONIS_COAT.jpg':							1,
	'MILK_SILK_GLOVES.jpg':							1,
	'MONTRENESS_SHOES.jpg':							3,
	'MURDERER’S_GLOVES.jpg':						2,
	'NIMBLE_GLOVES.jpg':							1,
	'POISON_PISTOL.jpg':							4,
	'RESONANCE_GOWN.jpg':							2,
	'RETICULATED_SWORD.jpg':						4,
	'RITTERSKIN_BOOTS.jpg':							2,
	'SEENTH_JACKET.jpg':							1,
	'SILENT_BOOTS.jpg':								2,
	'SLICKSLIPS.jpg':								2,
	'SLICKSUIT.jpg':								1,
	'SPIDERSILK_SUIT.jpg':							2,
	'SPIDERWEB_GLOVES.jpg':							3,
	'SPLINTERGOLD_SHIRT.jpg':						2,
	'STEALTHSUIT.jpg':								1,
	'TENTACLE_HAT.jpg':								2,
	'TENTACLE_UMBRELLA.jpg':						3,
	'TRASNIAN_CUFFLINK.jpg':						1,
	'TRASNIAN_EARRING.jpg':							1,
	'TRASNIAN_NECKLACE.jpg':						1,
	'TRASNIAN_RING.jpg':							1,
	'TRASNIAN_TIEPIN.jpg':							1,
	'TREFOIL.jpg':									4,
	'UNIKSKIN_COAT.jpg':							2,
	'VLINIAN_CAPE.jpg':								1,
	'WHISPERING_HAT.jpg':							2
}

class KindledItemsDeck(Deck):
    def __init__(self, card_path):
        Deck.__init__(self, KINDLED_ITEMS, card_path)


if __name__ == '__main__':
    pass
