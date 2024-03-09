import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@apollo/client';
import { GET_PRODUCTS, ADD_PRODUCT, REMOVE_PRODUCT, PRODUCT_ADDED_SUBSCRIPTION } from '../graphql/operations';
import { getAccessToken, signOut } from '../services/authService';

import { Box, VStack, Input, Button, Text, Heading, Container, UnorderedList, ListItem, useToast, IconButton } from "@chakra-ui/react";
import { FaPlus, FaTrash } from "react-icons/fa";

import { useBoolean } from "@chakra-ui/react";

interface Product {
  id: string;
  name: string;
}

interface GetProductsQuery {
  products: Product[];
}

// const HomePage: React.FC = () => {
//   const [newProductText, setNewProductText] = useState('');
//   const [pushToKafka, setPushToKafka] = useState(false);
//   const { data, loading, error, subscribeToMore } = useQuery(GET_PRODUCTS);
//   const [addProduct] = useMutation(ADD_PRODUCT);
//   const [removeProduct] = useMutation(REMOVE_PRODUCT);

//   useEffect(() => {
//     subscribeToMore({
//       document: PRODUCT_ADDED_SUBSCRIPTION,
//       updateQuery: (prev, { subscriptionData }) => {
//         if (!subscriptionData.data) return prev;
//         const newProduct = subscriptionData.data.productAdded;

//         if (prev.products.some((product: Product) => product.id === newProduct.id)) {
//           return prev;
//         }
//         return Object.assign({}, prev, {
//           products: [...prev.products, newProduct]
//         });
//       },
//     });
//   }, [subscribeToMore]);

//   if (loading) return (
//     <div className="flex justify-center items-center min-h-screen bg-base-300">
//       <button className="btn">
//         <span className="loading loading-spinner"></span>
//         Loading...
//       </button>
//     </div>
//   );
//   if (error) return <p>{'Error: ' + error}</p>;

//   const handleAddProduct = async () => {
//     if (!newProductText.trim()) return;
//     if (pushToKafka) {
//       const token = await getAccessToken();
//       const response = await fetch('/input/add_product', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'Authorization': token ? `Bearer ${token}` : "",
//         },
//         body: JSON.stringify({ name: newProductText }),
//       });
//       if (response.ok) {
//         setNewProductText('');
//       } else {
//         const errorText = await response.text();
//         console.error('Failed to add product:', errorText);
//       }
//     } else {
//       await addProduct({ variables: { name: newProductText } });
//       setNewProductText('');
//     }
//   };

//   const handleRemoveProduct = async (id: string) => {
//     await removeProduct({
//       variables: { id },
//       update(cache) {
//         const existingProducts = cache.readQuery<GetProductsQuery>({ query: GET_PRODUCTS });
//         if (existingProducts?.products) {
//           cache.writeQuery({
//             query: GET_PRODUCTS,
//             data: {
//               products: existingProducts.products.filter(product => product.id !== id),
//             },
//           });
//         }
//       },
//     });
//   };

//   return (
//     <div className="min-h-screen flex flex-col">
//       <div className="navbar bg-base-300 text-neutral-content">
//         <div className="flex-1">
//           <a href="/" className="p-2 normal-case text-xl">ProductLister</a>
//         </div>
//         <div className="flex-none">
//           <button className="btn" onClick={signOut}>
//           Sign out
//           </button>
//         </div>
//       </div>

//       <div className="flex flex-grow justify-center items-center bg-neutral">
//         <div className="card card-compact w-full max-w-lg bg-base-100 shadow-xl">
//           <div className="card-body items-stretch text-center">
//             <h1 className="card-title self-center text-2xl font-bold mb-4">Product List</h1>
//             <div className="form-control w-full">
//               <div className="join">
//                 <input
//                   type="text"
//                   placeholder="Add new product..."
//                   className="join-item flex-grow input input-bordered input-md input-primary"
//                   value={newProductText}
//                   onChange={(e) => setNewProductText(e.target.value)}
//                 />
//                 <button className="join-item btn btn-square btn-md btn-primary" onClick={handleAddProduct}>
//                   Add
//                 </button>
//               </div>
//             </div>
//             <div className="form-control w-full flex flex-row justify-center items-center">
//               <label className="join-item label">Submit directly</label>
//               <input type="checkbox" className="toggle mx-2" checked={pushToKafka} onChange={() => setPushToKafka(!pushToKafka)} />
//               <label className="join-item label">Submit via Kafka</label>
//             </div>
//             <div className="space-y-2 w-full">
//               {data.products.map(({ name, id }: Product) => (
//                 <div key={id} className="card card-compact w-full bg-base-200 flex-row items-center justify-between">
//                   <div className="card-body">
//                     <div className="flex justify-between items-center w-full">
//                       <span>{name}</span>
//                       <button className="btn btn-xs btn-circle btn-error" onClick={() => handleRemoveProduct(id)}>
//                         x
//                       </button>
//                     </div>
//                   </div>
//                 </div>
//               ))}
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// const HomePage: React.FC = () => {
//   const [isAdmin] = useBoolean(true);
//   const [ideas, setIdeas] = useState([]);
//   const [newIdea, setNewIdea] = useState("");
//   const [generatedIdea, setGeneratedIdea] = useState("");
//   const toast = useToast();

//   const generateIdea = () => {
//     setTimeout(() => {
//       setGeneratedIdea("This is a simulated brilliant idea generated by GPT-4.");
//     }, 1000);
//   };

//   const handleNewIdeaChange = (event: { target: { value: React.SetStateAction<string>; }; }) => {
//     setNewIdea(event.target.value);
//   };

//   const addIdea = () => {
//     if (newIdea.trim() !== "") {
//       setIdeas([...ideas, newIdea]);
//       setNewIdea("");
//       toast({
//         title: "Idea added.",
//         description: "Your idea has been added to the list.",
//         status: "success",
//         duration: 3000,
//         isClosable: true,
//       });
//     } else {
//       toast({
//         title: "Empty idea",
//         description: "Please enter an idea before submitting.",
//         status: "error",
//         duration: 3000,
//         isClosable: true,
//       });
//     }
//   };

//   const removeIdea = (index: number) => {
//     const newIdeas = [...ideas];
//     newIdeas.splice(index, 1);
//     setIdeas(newIdeas);
//   };

//   return (
//     <Container maxW="container.md" py={10} p={8}>
//       <VStack spacing={4} as="form" onSubmit={(e) => e.preventDefault()} align="center" mt={12}>
//         <Heading size="2xl">Idea Master</Heading>
//         <Text fontSize="xl">Share your ideas with the world!</Text>
//         <Input placeholder="What's your idea?" value={newIdea} onChange={handleNewIdeaChange} boxShadow="base" />
//         {isAdmin && (
//           <Button leftIcon={<FaPlus />} colorScheme="teal" onClick={addIdea}>
//             Add your thoughts
//           </Button>
//         )}
//       </VStack>
//       <Box mt={10}>
//         <Heading size="md" mb={4}>
//           Group thoughts
//         </Heading>
//         {ideas.length > 0 ? (
//           <UnorderedList>
//             {ideas.map((idea, index) => (
//               <ListItem key={index} d="flex" alignItems="center" mb={2}>
//                 {idea}
//                 {isAdmin && <IconButton icon={<FaTrash />} colorScheme="red" variant="ghost" aria-label="Delete Idea" onClick={() => removeIdea(index)} ml={2} />}
//               </ListItem>
//             ))}
//           </UnorderedList>
//         ) : (
//           <Text>No ideas yet. Be the first to submit!</Text>
//         )}
//       </Box>
//       {isAdmin && (
//         <Button colorScheme="orange" mt={6} size="lg" boxShadow="md" onClick={generateIdea}>
//           Generate a Brilliant Idea
//         </Button>
//       )}
//       <Text mt={4}>{generatedIdea}</Text> {}
//     </Container>
//   );
// };

const HomePage: React.FC = () => {
  const [isAdmin] = useBoolean(true);
  const [ideas, setIdeas] = useState<string[]>([]);
  const [newIdea, setNewIdea] = useState<string>("");
  const [generatedIdea, setGeneratedIdea] = useState<string>("");
  const toast = useToast();

  const generateIdea = () => {
    setTimeout(() => {
      setGeneratedIdea("This is a simulated brilliant idea generated by GPT-4.");
    }, 1000);
  };

  const handleNewIdeaChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setNewIdea(event.target.value);
  };

  const addIdea = () => {
    if (newIdea.trim() !== "") {
      setIdeas([...ideas, newIdea]);
      setNewIdea("");
      toast({
        title: "Idea added.",
        description: "Your idea has been added to the list.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } else {
      toast({
        title: "Empty idea",
        description: "Please enter an idea before submitting.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const removeIdea = (index: number) => {
    const newIdeas = [...ideas];
    newIdeas.splice(index, 1);
    setIdeas(newIdeas);
  };

  return (
    <Container maxW="container.md" py={10} p={8}>
      <VStack spacing={4} as="form" onSubmit={(e) => e.preventDefault()} align="center" mt={12}>
        <Heading size="2xl">Idea Master</Heading>
        <Text fontSize="xl">Share your ideas with the world!</Text>
        <Input placeholder="What's your idea?" value={newIdea} onChange={handleNewIdeaChange} boxShadow="base" />
        {isAdmin && (
          <Button leftIcon={<FaPlus />} colorScheme="teal" onClick={addIdea}>
            Add your thoughts
          </Button>
        )}
      </VStack>
      <Box mt={10}>
        <Heading size="md" mb={4}>
          Group thoughts
        </Heading>
        {ideas.length > 0 ? (
          <UnorderedList>
            {ideas.map((idea, index) => (
              <ListItem key={index} d="flex" alignItems="center" mb={2}>
                {idea}
                {isAdmin && <IconButton icon={<FaTrash />} colorScheme="red" variant="ghost" aria-label="Delete Idea" onClick={() => removeIdea(index)} ml={2} />}
              </ListItem>
            ))}
          </UnorderedList>
        ) : (
          <Text>No ideas yet. Be the first to submit!</Text>
        )}
      </Box>
      {isAdmin && (
        <Button colorScheme="orange" mt={6} size="lg" boxShadow="md" onClick={generateIdea}>
          Generate a Brilliant Idea
        </Button>
      )}
      <Text mt={4}>{generatedIdea}</Text>
    </Container>
  );
};

export default HomePage;
