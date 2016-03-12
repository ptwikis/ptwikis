
function imprimeTabela(conteudoTabela){

 for(i=0;i<Object.keys(repositorio.nome).length;i++){ 
  ////monta linha da tabela

var boldc = "";
var boldc2 = "";
var bolds = "";
var bolds2 = "";

if (commons[i]>0){boldc="<b>";boldc2="</b>";}
if (source[i]>0){bolds="<b>";bolds2="</b>";}

  var texto = "<tr><td><a href='http://"+repositorio["url"][i]+"'>"+repositorio["nome"][i]+" </a></td><td>"+boldc+commons[i]+boldc2+"</td> <td>"+bolds+source[i]+bolds2+"</td> </tr>";
  ////adiciona linha na tabela
  conteudoTabela += texto;
 }//fechar for
 conteudoTabela += "</table>";
 document.getElementById("tabela").innerHTML = conteudoTabela;
}

function somaValor(proj,elementos,indice){

if (proj == "source"){
		if (typeof source[indice] == 'undefined'){ 
		valorAtual = 0;
		} else {
		valorAtual = source[indice]; 
		}
		source[indice] = valorAtual + elementos;
}else{ //caso commons
		if (typeof window.commons[indice] == 'undefined'){ 
		valorAtual = 0;
		} else {
		valorAtual = window.commons[indice]; 
		}
		window.commons[indice] = valorAtual + elementos;

}// fim else

}// fim funcao somaValor


function rodaAPI(chamadaAPI, indice){

$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: chamadaAPI,
        contentType: "application/json; charset=utf-8",
        async: false,
        dataType: "jsonp",
        success: function (data, textStatus, jqXHR) {
// contar resultados e somar no objeto repositorio
		var elementos = data.query.exturlusage.length;
		if (typeof elementos === 'undefined'){elementos = 0;}
		var valorAtual;
		// obter o proj a partir de chamadaAPI
		if(chamadaAPI.search(/\./)==9){
		proj = "source";
		} else{proj = "commons";}

		if (proj == "source"){ // contar subpaginas e subtrair de elementos
		// for elementos
		// pegar data.query.exturlusage[indice].pagetitle
		// if com regex que procura "/" no nome 
		// caso sim, fazer elementos = elementos - 1
}
somaValor(proj,elementos,indice);


        }, //fecha function success
        error: function (errorMessage) {
		console.log(errorMessage);
        }
    });

});
}

//alimentar objeto com todas URL e nomes das bases


var repositorio = {nome: ["Banco Internacional de Objetos Educacionais","Copyleft Pearson Education","Curriculo+","Educopédia","Escola Digital","Portal do Professor","Portal Domínio Público","Secretaria Municipal de Educação de São Paulo","REA Dante","Porto OCW","Ambiente Educacional Web","Edukatu","Recursos educacionais multimídia para a matemática do ensino médio","FGV OCW","RIVED","Biblioteca Digital de Ciências","Edumatec","Klick Educação","LabVirt","Biblioteca Brasilianna Guita e José Mindlin","BVCH","Plataforma Democrática","Portal Dia a Dia da Educação","Acervo Multimeios","Fábrica Virtual - LEC","UFF CDME","Coursera","Khan Academy","Cláudio André.com.br","Química em Ação","Física Interativa","Scratch","Geekie","CESTA","FEB","Biblioteca Nacional Digital","ARCA","NOAS","Biblioteca Digital do Centro de Trabalho Indigenista"], url: ["objetoseducacionais2.mec.gov.br","copyleftpearson.com.br","curriculomais.educacao.sp.gov.br","educopedia.com.br","escoladigital.org.br","portaldoprofessor.mec.gov.br","dominiopublico.gov.br","portalsme.prefeitura.sp.gov.br","colegiodante.com.br/rea","ocw.portoseguro.org.br","ambiente.educacao.ba.gov.br","edukatu.org.br","m3.ime.unicamp.br","fgv.br/fgvonline/Cursos/Gratuitos","rived.mec.gov.br","bdc.ib.unicamp.br/bdc","mat.ufrgs.br/edumatec","klickeducacao.com.br","labvirt.futuro.usp.br","brasiliana.usp.br","bvce.org.br","plataformademocratica.org","diaadiaeducacao.pr.gov.br","multimeios.seed.pr.gov.br","lec.ufrgs.br","uff.br/cdme","coursera.org","pt.khanacademy.org","claudioandre.com.br","quimicaemacao.com.br","fisicainterativa.com","scratch.mit.edu","geekie.com.br","cinted.ufrgs.br/xmlui/","feb.ufrgs.br","bndigital.bn.br","arca.fiocruz.br","noas.com.br","bd.trabalhoindigenista.org.br"]};

// criar variaveis para chamadas de API
var projeto = ["commons.wikimedia", "pt.wikisource"];
var protocolo = ["http", "https"];
var namespace = [6,0];

var commons = [];
var source = [];

// criar variavel para receber o texto dinamico a ser exibido
var conteudoTabela = "<table border='1'><tr><td>Base de recursos</td><td>Uso no Commons</td><td>Uso no pt.wikisource</td></tr>";

var chamadaAPI;

//for elementos no objeto repositorio
for(i=0;i<Object.keys(repositorio.nome).length;i++){ 
 for(j=0;j<projeto.length;j++){ 
  for(k=0;k<protocolo.length;k++){ 
    var chamadaAPI = 'http://'+projeto[j]+'.org/w/api.php?format=json&action=query&list=exturlusage&euquery=*.'+repositorio["url"][i]+'&euprotocol='+protocolo[k]+'&eulimit=500&eunamespace='+namespace[j];
    rodaAPI(chamadaAPI, i);
console.log(chamadaAPI);
  }// fecha for k
 }//fecha for j
}//fecha for i


function imprimeDelay(){
    setTimeout(function(){ 
    imprimeTabela(conteudoTabela);
    }, 4500);  
}

imprimeDelay();

