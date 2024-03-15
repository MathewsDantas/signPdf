# DIRETRIZES PARA ASSINATURA DIGITAL DE DOCUMENTOS

Para garantir uma prática segura de assinatura de documentos com certificados, geralmente é recomendado seguir estas diretrizes:

- **Vinculação do Certificado ao Usuário:** Cada usuário deve ter seu próprio certificado digital, vinculado de forma segura à sua identidade.
  
- **Armazenamento Seguro do Certificado:** Os certificados dos usuários devem ser armazenados de forma segura, protegidos por senha e criptografados.
  
- **Utilização do Mesmo Certificado:** O sistema deve garantir que cada usuário utilize o mesmo certificado digital associado à sua identidade em todas as assinaturas.
  
- **Verificação de Integridade do Certificado:** Antes de permitir que um usuário assine um documento, o sistema deve verificar a integridade e validade do certificado digital.
  
- **Registro de Auditoria:** Todas as operações de assinatura de documentos devem ser registradas em um log de auditoria para rastreabilidade.

Em resumo, a prática adequada envolve garantir que cada usuário tenha seu próprio certificado digital, usado consistentemente, e registrar todas as operações para garantir a segurança do sistema.

# O PROBLEMA

A falha está na falta de vinculação do certificado ao usuário e na geração de um novo certificado a cada vez que o usuário assina um documento. O procedimento correto seria:

- **Geração do Certificado na Primeira Assinatura:** O sistema deve permitir que o usuário gere um certificado digital na primeira assinatura, único para ele.
  
- **Armazenamento Seguro do Certificado:** O certificado gerado deve ser armazenado de forma segura no banco de dados, protegido adequadamente.
  
- **Uso do Mesmo Certificado para Assinaturas Futuras:** O sistema deve utilizar o mesmo certificado associado ao usuário em futuras assinaturas.
  
- **Gerenciamento do Ciclo de Vida do Certificado:** Deve-se gerenciar o ciclo de vida dos certificados, permitindo renovação ou revogação conforme necessário.

# CLASSIFICAÇÃO SEGUINDO O OWASP TOP TEN

O problema descrito fere principalmente as seguintes boas práticas do OWASP Top Ten:

**A01:2021 - Broken Access Control:** Embora o problema não envolva diretamente o acesso não autorizado aos recursos, ele está relacionado à gestão inadequada dos certificados e à falta de controle sobre quem está assinando os documentos. A ausência de vinculação entre os certificados e os usuários pode permitir a manipulação inadequada dos certificados, comprometendo indiretamente o controle de acesso e a integridade dos documentos.  

**A05:2021 - Security Misconfiguration:** A prática de gerar novos certificados a cada assinatura de documento pode ser considerada uma configuração inadequada do sistema. Isso pode levar a vulnerabilidades, como falta de rastreabilidade e inconsistência nas assinaturas, o que pode facilitar ataques ou erros de segurança. 

Código referência: [CÓDIGO DA VIEW](https://imgur.com/a/qTswT4X)
