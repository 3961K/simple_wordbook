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
        q: '',
        next_page: false,
        previous_page: false,
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
                // 作者でないのに単語帳へカードを削除しようとした場合は403へリダイレクト
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

        // 単語帳に含まれているカードを取得する
        this.get_cards_per_page(1);
    },
    methods: {
        get_cards_per_page: function(page_number, with_q=false){
            // 指定したページ,パラメータを利用してユーザの情報の取得を行う
            let params = {page: page_number};
            if (with_q) {
                params['q'] = this.q;
            }
            axios.get(
                `/api/v1/wordbooks/${this.id}/cards/`,
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
        delete_card_from_wordbook: function(card_id, card_index) {
            // 削除するか確認
            let partial_card_word = this.cards_per_page[card_index].word.substring(0, 10);
            if (this.cards_per_page[card_index].word.substring(0, 10).length > 10) {
                partial_card_word += '...';
            }
            if (!window.confirm(`${partial_card_word}を単語帳から削除しますか?`)) {
                return;
            }
            // csrftokenを取得
            const csrftoken = $cookies.get('csrftoken');
            const headers = {'X-CSRFToken': csrftoken};
            // delete_cardsにcard_idを追加
            const params = {
                delete_cards: [card_id]
            }
            // 指定したカードを単語帳から削除
            axios.patch(
                `/api/v1/wordbooks/${this.id}/`, params, {headers: headers}
            )
            .then(response => {
                // カードの削除に成功した事を表示して,ページを再読み込み
                window.alert('単語帳からカードを削除しました。');
                location.reload();
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert('単語帳からカードの削除に失敗しました。');
            })
        },
        get_delete_cards_from_wordbook_url: function() {
            // 単語帳からカードを削除するページへのリンクを返す
            return `/settings/wordbooks/${this.id}/delete-cards/`
        },
        get_add_cards_to_wordbook_url: function() {
            // 単語帳にカードを追加するページへのリンクを返す
            return `/settings/wordbooks/${this.id}/add-cards/`
        },
        get_card_page_url: function(card_id) {
            // カードの詳細ページへのリンクを返す
            return `/cards/${card_id}/`;
        },
        get_edit_card_page_url: function(card_id) {
            // カードの詳細ページへのリンクを返す
            return `/settings/cards/${card_id}/`;
        },
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
    }
})