<script lang="ts">
	import { Form, FormGroup, Button, TextInput, Select, SelectItem } from 'carbon-components-svelte';

	export let full_name: string;
	export let pickup_location: string;
	export let destination_location: string;
	export let cost: number;

	const pickup_locations = ['None', 'London', 'Paris', 'Chicago', 'Boston', 'Seattle'];
	$: invalid_pickup = pickup_location == 'None' ? true : false;
	let destination_locations: Array<string> = [];
	function pickup_selected() {
		destination_locations = pickup_locations.filter((e) => e !== pickup_location && e !== 'None');
	}
	$: valid_form =
		pickup_location != 'None' &&
		destination_location != 'None' &&
		destination_location != undefined &&
		full_name != undefined
			? true
			: false;
</script>

<Form>
	<FormGroup>
		<TextInput
			invalid={full_name == undefined || full_name == ''}
			invalidText="Please set a name"
			size="xl"
			placeholder="Enter your Name"
			bind:value={full_name}
		/>
	</FormGroup>
	<FormGroup>
		<Select
			on:change={pickup_selected}
			invalid={invalid_pickup}
			invalidText="Can't be None"
			labelText="Choose pickup location"
			bind:selected={pickup_location}
		>
			{#each pickup_locations as location}
				<SelectItem value={location} />
			{/each}
		</Select>
	</FormGroup>
	<FormGroup>
		<Select
			labelText="Choose destination location"
			bind:selected={destination_location}
			disabled={invalid_pickup}
			invalid={invalid_pickup}
			invalidText="Pick a valid pickup location first"
			on:change
		>
			{#each destination_locations as location}
				<SelectItem value={location} />
			{/each}
		</Select>
	</FormGroup>
	<h2>Cost: £{cost}</h2>
	<Button disabled={!valid_form} on:click>Submit</Button>
</Form>

<style>
	h2 {
		padding-bottom: 1rem;
	}
</style>