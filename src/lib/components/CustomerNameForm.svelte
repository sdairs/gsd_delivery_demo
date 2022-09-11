<script lang="ts">
	import { Form, FormGroup, Button, TextInput } from 'carbon-components-svelte';

	export let customer_name: string | number | null;
</script>

<Form>
	<FormGroup>
		<TextInput size="xl" placeholder="Enter Customer Name" bind:value={customer_name} />
	</FormGroup>
	<Button disabled={customer_name == ''} on:click>Submit</Button>
</Form>
