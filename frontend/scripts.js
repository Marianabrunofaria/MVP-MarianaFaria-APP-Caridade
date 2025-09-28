// Cria um novo item na lista

function adicionarItem() {
  const novoItemInput = document.getElementById('novoItem');
  const nomeItem = novoItemInput.value;
  const corpoTabela = document.getElementById('corpoTabela');

  if (nomeItem === "") {
    alert("Por favor, insira um nome para o item.");
    return;
  }

  const novaLinha = corpoTabela.insertRow(); // Adiciona uma nova linha ao final da tabela
  const celulaNome = novaLinha.insertCell(0);
  const celulaAcoes = novaLinha.insertCell(1);

  celulaNome.textContent = nomeItem;

  // Cria o botão de excluir
  const botaoExcluir = document.createElement('button');
  botaoExcluir.textContent = 'Excluir';
  botaoExcluir.onclick = function() {
    excluirItem(this); // 'this' refere-se ao botão clicado
  };
  celulaAcoes.appendChild(botaoExcluir);

  novoItemInput.value = ''; // Limpa o campo de entrada
}

function excluirItem(botao) {
  // 'botao' é o botão que foi clicado.
  // Traz para cima (`.parentNode`) para encontrar a linha `tr`
  // e depois remove a linha do seu pai (`.parentNode`) que é o `tbody`
  const linhaParaRemover = botao.parentNode.parentNode;
  linhaParaRemover.remove(); // Remove o elemento `tr` da tabela
}
