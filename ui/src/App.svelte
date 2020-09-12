<script>
  let files;
  let companyData = [];
  let companyName = '';
  let officers = [];

  const uploadFile = (body) => {
    return fetch('http://localhost:5000/document', { // Your POST endpoint
      method: 'POST',
      body,
    }).then(data => data.json());
  }

  const handleSubmit = async (event) => {
    const formData  = new FormData();
    formData.append('file', files[0]);
    const data = await uploadFile(formData);
    const companyNumber = data.data[0];
    const resp = await lookupCompany(companyNumber);
    
    companyData = resp.company_data;
    companyName = resp.company_name[0];
    officers = resp.officers

    alert("Uploaded");
  }

  const lookupCompany = (companyNumber) => {
    return fetch(`http://localhost:5000/lookup?company_number=${companyNumber}`).then(data => data.json())
  }

</script>

<main>
	<h1>Upload Formation Document</h1>
  <form on:submit|preventDefault={handleSubmit} enctype="multipart/form-data">
    <input type="file" name="file" bind:files/>
    <button type="submit">Upload</button>
  </form>
  <ul>
    <li>{companyName}</li>
    <li><b>Officers</b></li>
    {#each officers as officer}
      <li>{officer.key}: {officer.value}</li>
    {/each}
    <li><b>Data</b></li>
    {#each companyData as data}
      <li>{data.key}: {data.value}</li>
    {/each}
  </ul>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 28px;
		font-weight: 100;
	}
  ul {
    max-width: 500px;
    text-align: left;
    margin: 20px auto;
  }
</style>
