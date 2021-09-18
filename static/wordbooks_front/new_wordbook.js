Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        q: '',
        new_wordbook_name: '',
        is_hidden: false,
        username: '',
        cards_per_page: [],
        cards_display_status: [],
        add_card_list: [],
        add_card_id_list: [],
        current_page_num: 0,
        next_page: false,
        previous_page: false,
        is_only_own_cards: false,
    },
    created: function() {
        // ユーザ名パラメータを初期化する
        this.username = document.getElementById('login_username').textContent;
        // インスタンス作成時に単語帳に含まれるカードなどのパラメータを初期化する
        this.get_cards_per_page(1);
    },
    methods: {
        create_new_wordbook: function() {
            // CSRFTokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // 送信する新規単語帳名,公開属性を設定
            const params = {
                'wordbook_name': this.new_wordbook_name,
                'is_hidden': this.is_hidden
            };
            // 指定された単語帳名で単語帳を作成
            axios.post(
                '/api/v1/wordbooks/', params, {headers: headers}
            )
            .then(response => {
                // 単語帳の作成に成功した場合は,add_cardsのカードをその単語帳に含める様に設定
                if (response.status == 201){
                    this.add_cards_to_new_wordbook(response.data.id);
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('単語帳の作成に失敗しました。');
            })
        },
        add_cards_to_new_wordbook: function (wordbook_id) {   
            // CSRFTokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // 新しく作成した単語帳にadd_card_id_listに格納されているカード番号群を設定
            const params = {
                'add_cards': this.add_card_id_list
            };
            // 作成した単語帳にカードを追加
            axios.patch(
                `/api/v1/wordbooks/${wordbook_id}/`, params, {headers: headers}
            )
            .then(response => {
                // カードの追加に成功した場合は成功した旨を表示し,各パラメータをクリアする
                if (response.status == 200){
                    this.add_card_id_list = [];
                    this.add_card_list = [];
                    this.new_wordbook_name = '';
                    this.is_hidden = false;
                    window.alert('単語帳の作成に成功しました');
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('単語帳へカードを追加する事に失敗しました。');
            })
        },
        get_cards_per_page: function(page_number, with_q=false){
            // 指定したページ,パラメータを利用してユーザの情報の取得を行う
            let params = {page: page_number};
            if (with_q) {
                params['q'] = this.q;
            }

            // is_only_own_cardsがTrueの場合は/api/v1/users/<str:username>/cardsにURLを変更する
            let url = '/api/v1/cards/';
            if (this.is_only_own_cards) {
                url = `/api/v1/users/${this.username}/cards/`;
            }
            axios.get(
                url,
                {
                    params: params
                }
            )
            .then(response => {
                if (response.status == 200){
                    this.cards_per_page = response.data.results;
                    this.cards_display_status = Array(this.cards_per_page.length);
                    this.cards_display_status.fill(true);
                    this.current_page_num = page_number;
                    this.next_page = response.data.next;
                    this.previous_page = response.data.previous;
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('カード情報の取得に失敗しました。');
            })
        },
        get_card_page_url: function(card_id) {
            return `/cards/${card_id}/`;
        },
        change_card_status: function(card) {
            // 既にadd_card_mapにカードが含まれている場合は削除し,存在しない場合は追加する
            const card_id = card.id;

            if (card_id in this.add_card_list) {
                this.$delete(this.add_card_list, card_id);
                this.add_card_id_list.splice(this.add_card_id_list.indexOf(card_id), 1);
                return;
            }

            const add_card_info = {
                'word': card.word,
                'answer': card.answer,
            };

            this.$set(this.add_card_list, card_id, add_card_info);
            this.add_card_id_list.push(card_id);
        }
    },
    computed: {
        card_display_status: function() {
            // 指定したカードの表示状態を返す
            return function(index) {
                return this.cards_display_status[index];
            }
        },
        card_content: function() {
            // 指定したカードの表示状態に基づいてwordまたはanswerを返す
            return function(index) {
                this.cards_display_status.splice(index, 1, !this.cards_display_status[index]);
            }
        }
    },
    watch: {
        // is_only_own_cardsが変更された瞬間にget_cards_per_page()を再度実行させる
        is_only_own_cards: function() {
            this.get_cards_per_page(1);
        }
    }
})