fn fatorial(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    return n * fatorial(n - 1);
}

fn main() {
    let num: int = 5;
    let resultado: int = fatorial(num);
    println("Fatorial de", num, "é", resultado);
}
