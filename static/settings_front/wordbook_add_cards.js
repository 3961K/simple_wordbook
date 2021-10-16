Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        username: '',
        id: '',
        wordbook_name: '',
        is_hidden: false,
        cards_per_page: [],
        cards_display_status: [],
        current_page_num: 0,
        is_only_own_cards: false,
        q: '',
        next_page: false,
        previous_page: false,
        add_card_list: [],
        add_card_id_list: [],
    },
    created: function() {
        // ユーザ名を取得
        this.username = document.getElementById('username').getAttribute('value');
        // 単語帳IDを取得
        this.id = window.location.pathname.split('/')[3];
        // 単語帳の情報を取得
        axios.get(
            `/api/v1/wordbooks/${this.id}/`,
        )
        .then(response => {
            if (response.status == 200){
                // 作者でないのに単語帳へカードを追加しようとした場合は403へリダイレクト
                if (this.username != response.data.author_name) {
                    window.location.href = '/error/403/';
                }
                this.wordbook_name = response.data.wordbook_name;
                this.is_hidden = response.data.is_hidden;
            }
        })
        .catch(error => {
            // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
            window.alert('単語帳情報の取得に失敗しました。');
        })

        // カード一覧を取得する
        this.get_cards_per_page(1);
    },
    methods: {
        get_cards_per_page: function(page_number, with_q=false){
            // 指定したページ,パラメータを利用してユーザの情報の取得を行う
            let params = {page: page_number};
            if (with_q) {
                params['q'] = this.q;
            }
            // is_only_own_cardsがTrueの場合は/api/v1/users/<str:username>/cardsにURLを変更する
            let url = `/api/v1/cards/?exclude_wordbook_id=${this.id}`;
            if (this.is_only_own_cards) {
                url = `/api/v1/users/${this.username}/cards/?exclude_wordbook_id=${this.id}`;
            }
            axios.get(
                url,
                {params: params}
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
        update_wordbook_info: function() {
            // csrftokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // 単語帳名と公開属性を設定
            const params = {
                wordbook_name: this.wordbook_name,
                is_hidden: this.is_hidden
            }
            // 単語帳名と公開属性を更新
            axios.patch(
                `/api/v1/wordbooks/${this.id}/`, params, {headers: headers}
            )
            .then(response => {
                // カードの削除に成功した事を表示して,ページを再読み込み
                window.alert('単語帳の情報を更新しました。');
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('単語帳の情報を更新に失敗しました。');
            })

        },
        add_cards_to_wordbook: function() {
            // csrftokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // delete_cardsにcard_idを追加
            const params = {
                add_cards: this.add_card_id_list
            };
            // 指定したカードを単語帳へ追加
            axios.patch(
                `/api/v1/wordbooks/${this.id}/`, params, {headers: headers}
            )
            .then(response => {
                // カードの追加に成功した事を表示して,ページを再読み込み
                window.alert('単語帳へカードを追加しました。');
                location.reload();
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('単語帳へのカードの追加に失敗しました。');
            })
        },
        get_delete_cards_from_wordbook_url: function() {
            // 単語帳からカードを削除するページへのリンクを返す
            return `/settings/wordbooks/${this.id}/delete-cards/`;
        },
        get_add_cards_to_wordbook_url: function() {
            // 単語帳にカードを追加するページへのリンクを返す
            return `/settings/wordbooks/${this.id}/add-cards/`;
        },
        get_card_page_url: function(card_id) {
            // カードの詳細ページへのリンクを返す
            return `/cards/${card_id}/`;
        },
        get_edit_card_page_url: function(card_id) {
            // カードの詳細ページへのリンクを返す
            return `/settings/cards/${card_id}/`;
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