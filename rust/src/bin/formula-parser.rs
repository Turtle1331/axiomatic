#![allow(dead_code)]

#[derive(Debug)]
enum LexerTokenType {
    Symbol,
    Bottom,
    Implies,
    OpenParens,
    CloseParens,
}

#[derive(Debug)]
struct LexerToken<'a> {
    token_type: &'a LexerTokenType,
    content: &'a str,
}

fn lex(blah: &str) -> Vec<LexerToken> {
    enum LexerState {
        None,
        Symbol,
        Bottom,
    }

    let mut tokens = Vec::new();
    let mut state = LexerState::None;
    let mut contents: String = String::new();

    for chr in blah.chars() {
        let split: bool = match chr {
            'A'..='Z' | 'a'..='z' => {
                state = LexerState::Symbol;
                false
            },
            ' ' | '-' | '>' => false,
            '(' => false,
            ')' => false,
            _ => {
                state = LexerState::None;
                true
            },
        };
        if split {
            tokens.push(LexerToken{
                token_type: &LexerTokenType::Implies,
                content: "",
            });
        }
        contents.push(chr);
    }

    tokens
}

fn main() {
    let prop_str = "(P -> bot)";
    let prop_tokens = lex(prop_str);
    println!("{:?}", prop_tokens);
}
