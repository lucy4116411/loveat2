# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## 1.0.0 (2019-12-07)


### ⚠ BREAKING CHANGES

* rename get_all_type to get_type

Before:
    get_all_type()
After:
    get_type(item=True, combo=True)
* change the post format of new order api

	Before:
	{
		"takenAt": "2019-10-31T12:00",
		"notes": "不要加番茄",
		"userName": "loveateat'
		"total": "500",
		"content": [
			{
				"id": "5dd67f098f0f6afb3ebc1b68",
				"category": "item",
				"quantity": 1
			},
			{
				"id": "5dd695b9fb8001b28236efb7",
				"category": "combo",
				"quantity": 1
			}
		]
	}
	After:
	{
		"takenAt": "2019-10-31T12:00",
		"notes": "不要加番茄",
		"total": "500",
		"content": [
			{
				"id": "5dd67f098f0f6afb3ebc1b68",
				"category": "item",
				"quantity": 1
			},
			{
				"id": "5dd695b9fb8001b28236efb7",
				"category": "combo",
				"quantity": 1
			}
		]
	}

### Features

* add default pic and favicon ([a93b494](https://github.com/creek0810/loveat2/commit/a93b4945a3f78136bacbbbcbcfcddd3d5aa8f2c1))
* add get all type function ([f377d32](https://github.com/creek0810/loveat2/commit/f377d32af062d067025e65ebebaf0b4afba80233))
* add the ability of setting business time ([28cde08](https://github.com/creek0810/loveat2/commit/28cde085db2811b94593c197aa9d8c6956e12d28))
* add undone menu ([9fa8c08](https://github.com/creek0810/loveat2/commit/9fa8c0894eae6cc22d5213c2b35111e1f52159ce))
* add update type test ([3a8d17e](https://github.com/creek0810/loveat2/commit/3a8d17eae7e6ba99f175efcbb6f53e3c883a8668))
* add updateQuantity function in cart.js ([103e49d](https://github.com/creek0810/loveat2/commit/103e49de4a227dba51014524437bbc9d0286c45b))
* change the status code return from admin_required ([4e8eca0](https://github.com/creek0810/loveat2/commit/4e8eca079cfa08bc500f10054903db2b9e0f8455))
* extend get_type function to search for only item or combo ([a06a78f](https://github.com/creek0810/loveat2/commit/a06a78f68266b01b4ec55294b65f68c907537404))
* finish add combo api ([17f260f](https://github.com/creek0810/loveat2/commit/17f260f645e4267a37632f7ba14a2eb2d2d0bbac))
* finish add, update type api ([640e107](https://github.com/creek0810/loveat2/commit/640e10792b1852cb4319d6d98aa5f090707349d6))
* finish all menu api ([50ab40d](https://github.com/creek0810/loveat2/commit/50ab40de731ef262335df74bb447bc77fd95b844))
* finish basic order history api ([e423987](https://github.com/creek0810/loveat2/commit/e423987373a077094d994b0965099edb431e38c7))
* finish business_time model and api ([4141ea1](https://github.com/creek0810/loveat2/commit/4141ea1101ee26d9a31361ae22041cdfcfcd714f))
* finish cart page UI layout ([07ba5d2](https://github.com/creek0810/loveat2/commit/07ba5d208aa3fa3d18dbdbb2f29092397d0ae04c))
* finish cart.js and cart page ([b751d62](https://github.com/creek0810/loveat2/commit/b751d6209ab084b7cd1d0aa96955f21f0bbcc339))
* finish customer front end push ([18550e9](https://github.com/creek0810/loveat2/commit/18550e9fa3189cd5fda724085bac8022745acce6))
* finish delete item, combo api ([082f3c6](https://github.com/creek0810/loveat2/commit/082f3c6e42e1ce63196d3b9ffbccc3b03aaafdfa))
* finish delete type and add item api ([5b83fe4](https://github.com/creek0810/loveat2/commit/5b83fe411ce0479a018fb33c27d44be3475d13d5))
* finish forget password ([1dbf2d0](https://github.com/creek0810/loveat2/commit/1dbf2d02eb386e480f3296d833b5760740cefe08))
* finish get item and combo api ([be38082](https://github.com/creek0810/loveat2/commit/be3808223acc355c896a034d5a7e2a29eae1b52e))
* finish get_unknown_order model func ([1cd6368](https://github.com/creek0810/loveat2/commit/1cd6368f297e832d0e9758a4cb122aec3c0f6bce))
* finish load data and display, without rwd ([b1f6062](https://github.com/creek0810/loveat2/commit/b1f6062967c15de1d88de3c8718c2a6130e9face))
* finish logout ([ee3b9a1](https://github.com/creek0810/loveat2/commit/ee3b9a171b8ed821dbf472f3482923d0317aa312))
* finish menu feature ([1e9e28a](https://github.com/creek0810/loveat2/commit/1e9e28ac33699f1adb3a2c2335e8109a6c2b6c11))
* finish menu localStorage ([3a600de](https://github.com/creek0810/loveat2/commit/3a600de2bec1bb0f88a2ded9d35757e721dc231e))
* finish model op for customer state page ([c0810ae](https://github.com/creek0810/loveat2/commit/c0810ae9856770a086646c2ad4a44e1fe5036140))
* finish navbar and layout ([31f611e](https://github.com/creek0810/loveat2/commit/31f611e9de54b650fe6faec955243d79da686fd8))
* finish new order api ([ca9b8de](https://github.com/creek0810/loveat2/commit/ca9b8de1fe116cad6e48b5413b502827d8cceb40))
* finish new order push ([329ffe3](https://github.com/creek0810/loveat2/commit/329ffe34457d0c16f06a370647757e02c1cfb25d))
* finish push lib ([7f7cf94](https://github.com/creek0810/loveat2/commit/7f7cf94053cb1321f2b06ac22c6e178d00a6aee7))
* finish push notification for customer ([01e3f27](https://github.com/creek0810/loveat2/commit/01e3f2795c4cbba2ac49736429c932cafe4e3559))
* finish register, login, forgetpassword api ([36ca9ea](https://github.com/creek0810/loveat2/commit/36ca9ea94e6e72ced933af58977a715428ddd220))
* finish reset password and rename forget password function ([46fbf73](https://github.com/creek0810/loveat2/commit/46fbf734f9feafaf7c791a36061e37b609447e96))
* finish update order push ([a3009f7](https://github.com/creek0810/loveat2/commit/a3009f78d5c27a79f8312b5681f2598a818721de))
* **business_time:** add the ability of setting business time ([f3e99cc](https://github.com/creek0810/loveat2/commit/f3e99ccfdd1d179d313bf019b801b81cec8bc012))
* finish image route ([12b9771](https://github.com/creek0810/loveat2/commit/12b977102ba95e96c145bf3383062cb7d53b4095))
* finish todo order model and api ([17b06da](https://github.com/creek0810/loveat2/commit/17b06da692388080263d03bc1cd20fb2379faa0e))
* finish update combo, item api ([5ee16f2](https://github.com/creek0810/loveat2/commit/5ee16f2cfaf85f8f7709e4153569838146351f22))
* finish update order state api ([1116b50](https://github.com/creek0810/loveat2/commit/1116b5017e8a508aebc331eb836e51f0332e4534))
* finish update password api ([0a672c7](https://github.com/creek0810/loveat2/commit/0a672c7cc553fc11c8195d536fc1273f3ffa47cf))
* finish update profile api ([3bead13](https://github.com/creek0810/loveat2/commit/3bead1399f4dbf3eed2c6cb17d164753e5e55baf))
* finish update token api ([59097d1](https://github.com/creek0810/loveat2/commit/59097d18c343e6e422d343736fc3cfed07858ac9))
* finishh analysis api ([f66653e](https://github.com/creek0810/loveat2/commit/f66653e69dfd316546bce2cdc62ee89291f09d91))
* optimize UI, and block logined user to use forget-password ([b3af10f](https://github.com/creek0810/loveat2/commit/b3af10f2f881ac79bfdf8e4d675f471a9f2ec85b))
* rwd & delete itemPieChart ([fa84d3e](https://github.com/creek0810/loveat2/commit/fa84d3ea3aea76d72eca0de4fbbb7aa32aa13c34))
* use auth to manage history api ([bc4e494](https://github.com/creek0810/loveat2/commit/bc4e49481ee3d3d2d244e95066b27acabf104075))
* use lozad to speed up loading in menu page ([6119f33](https://github.com/creek0810/loveat2/commit/6119f33e8dde0b172879e116cea306c7c93f4362)), closes [#47](https://github.com/creek0810/loveat2/issues/47)


### Bug Fixes

* add login user attr making navbar show correct user ([e5836c4](https://github.com/creek0810/loveat2/commit/e5836c439f8da9053f7d4e599f8e0d6471ba6ae2))
* adding menu failed when order collection is empty ([ee5f19b](https://github.com/creek0810/loveat2/commit/ee5f19b180532b13af4ea626b9d6df6e0bfae711)), closes [#33](https://github.com/creek0810/loveat2/issues/33)
* change api url from absolute to relative in auth.js ([e89525d](https://github.com/creek0810/loveat2/commit/e89525d9a6417013e80f641a619bcf9b7ccbe9e3))
* change datetime format of get_not_end_by_username ([7d508eb](https://github.com/creek0810/loveat2/commit/7d508eb55438913594ce1dd8da89b4505a5b5843))
* change port=8080 and menu hint message ([0d8348a](https://github.com/creek0810/loveat2/commit/0d8348ade42581f83d1299217f1cf4f271b8874c))
* change the post format of new order api ([d65b472](https://github.com/creek0810/loveat2/commit/d65b47265cbea6375f97ce8f6776bdb5a7b1d97f))
* change token expired time in reset password email ([57fe2e8](https://github.com/creek0810/loveat2/commit/57fe2e862d5105e7236036b4084eecf68ec02492)), closes [#32](https://github.com/creek0810/loveat2/issues/32)
* fix adding nonexist order crash ([cd138ea](https://github.com/creek0810/loveat2/commit/cd138ea0193c389f903753e2efe7d52bc3a946c3))
* fix cart item quantity and register age value [#45](https://github.com/creek0810/loveat2/issues/45) [#46](https://github.com/creek0810/loveat2/issues/46) ([1760686](https://github.com/creek0810/loveat2/commit/176068625d528a9448b59f5a4613af28ad9f59e4))
* fix cors ([6980583](https://github.com/creek0810/loveat2/commit/69805835883eb9dd2c47a5714af48431755fa48b))
* fix user.find projection ([5331de9](https://github.com/creek0810/loveat2/commit/5331de9208205a0d8983e8be952f12b3876c7301))
* modify business time ([18e4ec4](https://github.com/creek0810/loveat2/commit/18e4ec4faf12b321a9484271550cba909065eb44))
* rewrite and conform to the format ([28c634d](https://github.com/creek0810/loveat2/commit/28c634d67eec15780f864e97dd0032e49c4deb63))
* server broken when push to empty token user and status code for ([c633235](https://github.com/creek0810/loveat2/commit/c633235c51b46762b1be428122e87a2ea76c1226))
* server error when adding no pic item or combo ([ba08f9d](https://github.com/creek0810/loveat2/commit/ba08f9d7fcb718645bbed2dbe8d89c245fbe0ace))
* show hint msg when login with nonexist user ([92a795e](https://github.com/creek0810/loveat2/commit/92a795e549cd6de772aa4cd23d4245785ccb5d85))
* table on gender display ([b5f66c9](https://github.com/creek0810/loveat2/commit/b5f66c9d99034ed8afb1d6804b1f055ae83dbce3))
* total update and duplicate add ([de47816](https://github.com/creek0810/loveat2/commit/de47816a1c8ec3fc1d543ffec7c94643afaec946))
