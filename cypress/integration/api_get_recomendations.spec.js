function checkResponse(resp)  {
  return ({body, status}) => {
    expect(status).is.equal(200)
    expect(body, 'response array')
      .to.be.a('array')
      .to.have.lengthOf(5)
    body.every(i => expect(i).to.have.property('recommendation'))
    // проверка наличия строки в ответе
    expect(body.some(i => i.recommendation === resp)).is.true
  };
}

it('GetRecommendations: shell', () => {
  cy.api(
    {
      url: '/DSS/GetRecommendations',
      body: {
        // строка запрашиваемая
        problemDescription: 'shell'
      },
      method: 'POST',
    }
  ).then(checkResponse("Проверьте правильность введенной команды"))
})

it('GetRecommendations: диск', () => {
  cy.api(
    {
      url: '/DSS/GetRecommendations',
      body: {
        // строка запрашиваемая
        problemDescription: 'диск'
      },
      method: 'POST',
    }
  ).then(checkResponse("Проверьте правильность введенной команды"))
})

