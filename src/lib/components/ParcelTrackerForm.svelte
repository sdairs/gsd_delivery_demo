<script lang="ts">
	import { Form, FormGroup, Button, TextInput } from 'carbon-components-svelte';

	export let order_id: string | number | null;
</script>

<Form>
	<FormGroup>
		<TextInput size="xl" placeholder="Enter Order ID" bind:value={order_id} />
	</FormGroup>
	<Button disabled={order_id == ''} on:click>Submit</Button>
</Form>
