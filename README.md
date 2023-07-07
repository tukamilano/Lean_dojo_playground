# Lean_dojo_playground

このコードはmathlibのデータをReproverを使って幅優先探索することで(state, action, next_state, reward)と(state, reward)のデータを得られる、木構造を用いたアルゴリズムです。(HTPSより単純に書きました)

mathlib4使えば10Mのデータセットを作るのも夢じゃなさそう

HTPSを使う前にこのコードとmathlibの定理からとりあえずデータを生み出し、reward(critic) modelを訓練するのはありかも

これでreward modelを事前学習したのちHTPSを回す(ミーティングの話し合いで出てきたことも実装できるようにしたい)

## rewardの設計(大枠)

HTPSより単純でreward modelを使わない方法を考えてみました

next_stateがエラーを吐いたらrewardは-1

証明が完了したらrewardは1、そして木構造の先祖ノードへrewardの更新を行う

## instruction

まずLean4が動く状態にしてください

pip install transformersをしたのち

python /interact/searchtree2.pyを実行してください