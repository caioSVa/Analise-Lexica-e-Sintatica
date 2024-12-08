fn calcular_media(valores: Σ+) -> float {
    let soma: float = 0.0;
    let tamanho: int = 0;

    while (valores[tamanho] != '\0') {
        soma = soma + valores[tamanho];
        tamanho = tamanho + 1;
    }

    return soma / tamanho;
}

fn main() {
    let numeros: Σ+ = {10.5, 20.0, 30.5, 40.0, '\0'};
    let media: float = calcular_media(numeros);

    println("Média dos valores:", media);
}
